# Resume to Portfolio - Quick Reference

## Quick Start (3 Steps)

### 1. Setup
```powershell
cd c:\Users\IRM99K\ashwin\r2p
.\setup.ps1
```

### 2. Configure
Edit `.env` file with your credentials:
- GitHub Client ID & Secret → https://github.com/settings/developers
- Perplexity API Key → https://www.perplexity.ai/settings/api
- Generate Secret Key → `python -c "import secrets; print(secrets.token_hex(32))"`

### 3. Run
```powershell
.\run.ps1
```
Then open: http://localhost:5000

---

## Project Structure

```
r2p/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env                      # Your credentials (create from .env.example)
│
├── utils/
│   ├── resume_parser.py      # PDF/DOC parsing + sanitization
│   └── portfolio_generator.py # Perplexity API integration
│
├── templates/
│   ├── login.html           # GitHub login page
│   ├── upload.html          # Resume upload page
│   └── result.html          # Preview & download page
│
├── uploads/                 # Temporary resume storage
└── generated/               # Generated portfolio HTML files
```

---

## Key Features Implemented

✅ **GitHub OAuth Authentication**
- Login/logout functionality
- Secure session management
- Redirects to GitHub signup if no account

✅ **Resume Upload & Parsing**
- Supports PDF, DOC, DOCX
- Max 16MB file size
- Drag-and-drop interface

✅ **Privacy Protection**
- Removes phone numbers
- Removes street addresses
- Removes PO boxes
- Email addresses kept for portfolio

✅ **Perplexity AI Integration**
- Generates professional HTML portfolios
- Single standalone HTML file
- Embedded CSS styling

✅ **Preview & Download**
- Live preview in iframe
- One-click download
- Clean filename

---

## Common Commands

### Activate Virtual Environment
```powershell
.\venv\Scripts\Activate.ps1
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Run Application
```powershell
python app.py
```

### Check Python Version
```powershell
python --version
```

### Deactivate Virtual Environment
```powershell
deactivate
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page (redirects based on auth) |
| `/login` | GET | Display login page |
| `/auth/github` | GET | Redirect to GitHub OAuth |
| `/callback` | GET | GitHub OAuth callback |
| `/logout` | GET | Logout user |
| `/upload` | GET | Display upload page |
| `/process` | POST | Process resume & generate portfolio |
| `/preview/<id>` | GET | Preview generated portfolio |
| `/download/<id>` | GET | Download portfolio HTML |
| `/result` | GET | Display result page |

---

## File Formats Supported

| Format | Extension | Library Used |
|--------|-----------|--------------|
| PDF | `.pdf` | PyPDF2, pdfplumber |
| Word 97-2003 | `.doc` | python-docx |
| Word 2007+ | `.docx` | python-docx |

---

## Environment Variables

| Variable | Purpose | Where to Get |
|----------|---------|--------------|
| `SECRET_KEY` | Flask session security | Generate with Python |
| `GITHUB_CLIENT_ID` | GitHub OAuth | GitHub Developer Settings |
| `GITHUB_CLIENT_SECRET` | GitHub OAuth | GitHub Developer Settings |
| `GITHUB_REDIRECT_URI` | OAuth callback | Usually `http://localhost:5000/callback` |
| `PERPLEXITY_API_KEY` | AI generation | Perplexity API Settings |

---

## Troubleshooting Quick Fixes

### Can't activate virtual environment
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port 5000 already in use
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Module not found errors
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall
```

### GitHub OAuth fails
- Check Client ID & Secret in `.env`
- Verify callback URL: `http://localhost:5000/callback`
- Clear browser cookies

### PDF parsing fails
```powershell
pip install --upgrade PyPDF2 pdfplumber
```

---

## Testing Checklist

- [ ] Login with GitHub works
- [ ] Upload PDF resume works
- [ ] Upload DOCX resume works
- [ ] Portfolio generation completes
- [ ] Preview displays correctly
- [ ] Download works
- [ ] Sensitive data removed from portfolio
- [ ] Logout works

---

## Security Notes

🔒 **What's Protected:**
- Phone numbers removed
- Street addresses removed
- PO boxes removed
- Secure session management
- File type validation
- File size limits

✉️ **What's Kept:**
- Email addresses (useful for contact)
- Names
- Professional information
- Work experience
- Education
- Skills

---

## Performance Tips

- Resume processing: ~10-30 seconds
- Perplexity API call: ~20-60 seconds
- Total time: ~30-90 seconds per resume
- Larger resumes take longer
- API rate limits may apply

---

## Need More Help?

📖 **Detailed Guides:**
- `README.md` - Complete project documentation
- `SETUP_GUIDE.md` - Step-by-step setup instructions

💻 **Code Documentation:**
- `app.py` - Main application with inline comments
- `utils/resume_parser.py` - Parsing logic
- `utils/portfolio_generator.py` - AI generation

---

**Version**: 1.0  
**Last Updated**: November 2025
