import os
from dotenv import load_dotenv
import tempfile

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for Flask application"""
    
    # Flask Settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # GitHub OAuth Settings
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    GITHUB_PASS = "mypassword@12345"
    GITHUB_AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
    GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    GITHUB_USER_API_URL = 'https://api.github.com/user'
    GITHUB_REPOS_API_URL = 'https://api.github.com/user/repos'
    
    # Perplexity API Settings
    PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
    PERPLEXITY_API_URL = 'https://api.perplexity.ai/chat/completions'
    PERPLEXITY_MODEL = 'sonar'  # Using the correct model name
    
    # File Upload Settings
    TEMP_DIR = tempfile.gettempdir()

    UPLOAD_FOLDER = os.path.join(TEMP_DIR, 'uploads')
    GENERATED_FOLDER = os.path.join(TEMP_DIR, 'generated')
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max file size
    
    # Color Themes for Portfolio
    COLOR_THEMES = {
        'professional-blue': {
            'primary': '#2C3E50',
            'secondary': '#3498DB',
            'accent': '#1ABC9C',
            'background': '#ECF0F1',
            'text': '#2C3E50'
        },
        'elegant-purple': {
            'primary': '#6C5CE7',
            'secondary': '#A29BFE',
            'accent': '#FD79A8',
            'background': '#F8F9FA',
            'text': '#2D3436'
        },
        'modern-green': {
            'primary': '#00B894',
            'secondary': '#00CEC9',
            'accent': '#FDCB6E',
            'background': '#DFE6E9',
            'text': '#2D3436'
        },
        'classic-gray': {
            'primary': '#2D3436',
            'secondary': '#636E72',
            'accent': '#D63031',
            'background': '#F8F9FA',
            'text': '#2D3436'
        }
    }
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_config():
        """Validate required environment variables"""
        required_vars = ['GITHUB_CLIENT_ID', 'GITHUB_CLIENT_SECRET', 'PERPLEXITY_API_KEY']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")
        
        return True
