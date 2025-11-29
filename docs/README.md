# Resume to Portfolio - Professional Portfolio Generator

Transform your resume into a beautiful, professional portfolio website with just a few clicks!
 
## 🌟 Features 

- **GitHub OAuth Authentication** - Secure login with your GitHub account
- **Resume Upload** - Support for PDF and DOCX formats
- **4 Professional Themes** - Choose from carefully crafted color schemes
- **AI-Powered Generation** - Uses Perplexity API for intelligent portfolio creation
- **Privacy-First** - Personal data (phone, address) is filtered before API calls
- **Instant Preview** - See your portfolio before downloading
- **Single HTML File** - Complete, self-contained, responsive portfolio
- **Download Ready** - Host anywhere - GitHub Pages, Netlify, or your own server

## 📋 Requirements

- Python 3.8+
- GitHub Account (for OAuth)
- GitHub OAuth App credentials
- Perplexity API key

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd r2p
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or on Windows:
```powershell
.\setup.ps1
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Generate a secret key:
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-generated-secret-key

# GitHub OAuth App credentials
# Create at: https://github.com/settings/developers
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret

# Perplexity API Key
# Get from: https://www.perplexity.ai/settings/api
PERPLEXITY_API_KEY=your-perplexity-api-key
```

### 4. Set Up GitHub OAuth App

1. Go to https://github.com/settings/developers
2. Click "New OAuth App"
3. Fill in the details:
   - **Application name**: Resume to Portfolio
   - **Homepage URL**: http://localhost:5000
   - **Authorization callback URL**: http://localhost:5000/callback
4. Copy the Client ID and Client Secret to your `.env` file

### 5. Get Perplexity API Key

1. Sign up at https://www.perplexity.ai/
2. Go to https://www.perplexity.ai/settings/api
3. Generate an API key
4. Copy it to your `.env` file

### 6. Run the Application

```bash
python app.py
```

Or on Windows:
```powershell
.\run.ps1
```

The app will be available at http://localhost:5000

## 📖 Usage

1. **Login** - Click "Sign in with GitHub" on the landing page
2. **Upload Resume** - Choose your PDF or DOCX resume file
3. **Select Theme** - Pick from 4 professional color themes:
   - Professional Blue
   - Elegant Purple
   - Modern Green
   - Classic Gray
4. **Generate** - Click "Generate Portfolio" and wait (~30-60 seconds)
5. **Preview** - View your portfolio in a new tab
6. **Download** - Save the HTML file to your computer
7. **Deploy** - Host on any web server or static hosting service

## 🏗️ Project Structure

```
r2p/
├── app.py                 # Main Flask application
├── config.py              # Configuration and settings
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── utils/
│   ├── resume_parser.py   # Resume parsing with privacy filtering
│   └── portfolio_generator.py  # Perplexity API integration
├── templates/
│   ├── login.html         # Login page
│   ├── upload.html        # Resume upload and theme selection
│   └── result.html        # Result page with preview/download
├── static/
│   └── css/              # Additional CSS if needed
├── uploads/              # Temporary resume storage
└── generated/            # Generated portfolio files
```

## 🔒 Security & Privacy

- **Personal Data Protection**: Phone numbers, addresses, and ZIP codes are filtered out before sending to the API
- **Session-Based Auth**: User sessions are securely managed
- **Temporary Files**: Uploaded resumes are deleted after processing
- **No Data Storage**: No personal information is permanently stored

## 🎨 Color Themes

### Professional Blue
- Primary: #2C3E50
- Secondary: #3498DB
- Accent: #1ABC9C

### Elegant Purple
- Primary: #6C5CE7
- Secondary: #A29BFE
- Accent: #FD79A8

### Modern Green
- Primary: #00B894
- Secondary: #00CEC9
- Accent: #FDCB6E

### Classic Gray
- Primary: #2D3436
- Secondary: #636E72
- Accent: #D63031

## 🛠️ Technical Details

### Resume Parsing
- Extracts text from PDF using PyPDF2
- Extracts text from DOCX using python-docx
- Regex-based filtering for personal data
- Section detection for structured parsing

### Portfolio Generation
- Uses Perplexity AI API (sonar model)
- Structured prompts for consistency and reproducibility
- Temperature 0.2 for consistent outputs
- Generates complete, self-contained HTML with inline CSS
- Mobile-responsive design
- Print-friendly styles

### Technologies
- **Backend**: Flask 3.0
- **Authentication**: GitHub OAuth 2.0
- **AI**: Perplexity API
- **Resume Parsing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## 🐛 Troubleshooting

### "Configuration Error: Missing required environment variables"
- Ensure your `.env` file exists and contains all required variables
- Check that variable names match exactly (case-sensitive)

### "Authentication failed"
- Verify GitHub OAuth App callback URL is set to `http://localhost:5000/callback`
- Check that Client ID and Secret are correct in `.env`

### "Failed to generate portfolio"
- Verify Perplexity API key is valid and has credits
- Check your internet connection
- Ensure resume file is not corrupted or password-protected

### "Unable to extract content from resume"
- Try converting your resume to PDF or DOCX format
- Ensure the resume file is not password-protected
- Check that the file contains readable text (not just images)

## 📝 Development Notes

### Adding New Themes
Edit `config.py` and add to `COLOR_THEMES` dict:

```python
'new-theme': {
    'primary': '#000000',
    'secondary': '#111111',
    'accent': '#222222',
    'background': '#FFFFFF',
    'text': '#000000'
}
```

### Customizing Portfolio Structure
Edit the system prompt in `utils/portfolio_generator.py` to modify the portfolio structure and design guidelines.

### Deployment Considerations
For production deployment:
1. Set `debug=False` in `app.py`
2. Use a production WSGI server (gunicorn, uwsgi)
3. Set up HTTPS
4. Update GitHub OAuth callback URL to production domain
5. Use environment-specific configuration
6. Set up proper logging

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

This is a complete, production-ready application. Feel free to fork and customize for your needs!

## 📧 Support

For issues or questions, please open an issue in the GitHub repository.

---

**Built with ❤️ using Flask, GitHub OAuth, and Perplexity AI**
