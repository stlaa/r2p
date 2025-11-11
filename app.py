import os
import uuid
import requests
from flask import Flask, render_template, request, redirect, url_for, session, send_file, jsonify
from werkzeug.utils import secure_filename
from config import Config
from utils.resume_parser import ResumeParser
from utils.portfolio_generator import PortfolioGenerator

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure required directories exist
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.GENERATED_FOLDER, exist_ok=True)

# Validate configuration on startup
try:
    Config.validate_config()
except ValueError as e:
    print(f"Configuration Error: {e}")
    print("Please check your .env file and ensure all required variables are set.")


# ============================================================================
# ROUTES - Authentication
# ============================================================================

@app.route('/')
def index():
    """Landing page - redirect to login if not authenticated"""
    if 'user' in session:
        return redirect(url_for('upload'))
    return redirect(url_for('login'))


@app.route('/login')
def login():
    """Login page with GitHub OAuth"""
    if 'user' in session:
        return redirect(url_for('upload'))
    return render_template('login.html')


@app.route('/auth/github')
def github_auth():
    """Initiate GitHub OAuth flow"""
    github_auth_url = (
        f"{Config.GITHUB_AUTHORIZATION_BASE_URL}"
        f"?client_id={Config.GITHUB_CLIENT_ID}"
        f"&scope=user:email"
        f"&redirect_uri={request.url_root}callback"
    )
    return redirect(github_auth_url)


@app.route('/callback')
def github_callback():
    """GitHub OAuth callback handler"""
    code = request.args.get('code')
    
    if not code:
        return render_template('login.html', error='Authentication failed. Please try again.')
    
    # Exchange code for access token
    token_response = requests.post(
        Config.GITHUB_TOKEN_URL,
        headers={'Accept': 'application/json'},
        data={
            'client_id': Config.GITHUB_CLIENT_ID,
            'client_secret': Config.GITHUB_CLIENT_SECRET,
            'code': code
        }
    )
    
    if token_response.status_code != 200:
        return render_template('login.html', error='Failed to authenticate with GitHub.')
    
    token_data = token_response.json()
    access_token = token_data.get('access_token')
    
    if not access_token:
        return render_template('login.html', error='Failed to obtain access token.')
    
    # Get user information
    user_response = requests.get(
        Config.GITHUB_USER_API_URL,
        headers={'Authorization': f'token {access_token}'}
    )
    
    if user_response.status_code != 200:
        return render_template('login.html', error='Failed to fetch user information.')
    
    user_data = user_response.json()
    
    # Store user info in session
    session['user'] = {
        'id': user_data.get('id'),
        'username': user_data.get('login'),
        'name': user_data.get('name', user_data.get('login')),
        'avatar': user_data.get('avatar_url'),
        'access_token': access_token
    }
    
    return redirect(url_for('upload'))


@app.route('/logout')
def logout():
    """Logout user and clear session"""
    session.clear()
    return redirect(url_for('login'))


# ============================================================================
# ROUTES - Main Application
# ============================================================================

@app.route('/upload')
def upload():
    """Upload page for resume and theme selection"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return render_template(
        'upload.html',
        user=session['user'],
        themes=Config.COLOR_THEMES
    )


@app.route('/generate', methods=['POST'])
def generate():
    """Generate portfolio from uploaded resume"""
    if 'user' not in session:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    # Check if file was uploaded
    if 'resume' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'}), 400
    
    if not Config.allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file format. Please upload PDF or DOCX file.'
        }), 400
    
    # Get selected theme
    theme = request.form.get('theme', 'professional-blue')
    
    if theme not in Config.COLOR_THEMES:
        theme = 'professional-blue'
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Parse resume
        parsed_data = ResumeParser.parse(file_path)
        
        if not parsed_data['has_content']:
            os.remove(file_path)
            return jsonify({
                'success': False,
                'error': 'Unable to extract content from resume.'
            }), 400
        
        # Generate portfolio using filtered content
        generator = PortfolioGenerator(
            Config.PERPLEXITY_API_KEY,
            Config.PERPLEXITY_API_URL,
            Config.PERPLEXITY_MODEL
        )
        
        # Get the color theme dictionary
        color_theme = Config.COLOR_THEMES.get(theme, Config.COLOR_THEMES['professional-blue'])
        
        result = generator.generate_portfolio(
            parsed_data['filtered_text'],
            color_theme
        )
        
        if not result['success']:
            os.remove(file_path)
            return jsonify({
                'success': False,
                'error': result.get('error', 'Failed to generate portfolio')
            }), 500
        
        # Save generated portfolio
        portfolio_filename = f"{uuid.uuid4()}_portfolio.html"
        portfolio_path = os.path.join(Config.GENERATED_FOLDER, portfolio_filename)
        
        if not generator.save_portfolio(result['html'], portfolio_path):
            os.remove(file_path)
            return jsonify({
                'success': False,
                'error': 'Failed to save portfolio'
            }), 500
        
        # Clean up uploaded file
        os.remove(file_path)
        
        # Store portfolio info in session
        session['portfolio'] = {
            'filename': portfolio_filename,
            'path': portfolio_path,
            'theme': theme
        }
        
        return jsonify({
            'success': True,
            'redirect': url_for('result')
        })
        
    except Exception as e:
        # Clean up files if they exist
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            'success': False,
            'error': f'Error processing resume: {str(e)}'
        }), 500


@app.route('/result')
def result():
    """Display result page with preview and download options"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if 'portfolio' not in session:
        return redirect(url_for('upload'))
    
    return render_template(
        'result.html',
        user=session['user'],
        portfolio=session['portfolio']
    )


@app.route('/preview/<filename>')
def preview(filename):
    """Preview generated portfolio"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    file_path = os.path.join(Config.GENERATED_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return "Portfolio not found", 404
    
    # Read and return HTML content
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return html_content


@app.route('/download/<filename>')
def download(filename):
    """Download generated portfolio"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    file_path = os.path.join(Config.GENERATED_FOLDER, filename)
    
    if not os.path.exists(file_path):
        return "Portfolio not found", 404
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name='portfolio.html',
        mimetype='text/html'
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors"""
    return render_template('login.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors"""
    return render_template('login.html', error='Internal server error'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
