# Complete Setup Guide - Resume to Portfolio

This guide will walk you through setting up the Resume to Portfolio application from scratch.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [GitHub OAuth Setup](#github-oauth-setup)
4. [Perplexity API Setup](#perplexity-api-setup)
5. [Running the Application](#running-the-application)
6. [Testing the Application](#testing-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Python 3.8+**: [Download here](https://www.python.org/downloads/)
- **Git** (optional): [Download here](https://git-scm.com/downloads)
- **GitHub Account**: [Sign up here](https://github.com/signup)

### Required API Keys
- GitHub OAuth credentials (Client ID and Secret)
- Perplexity API key

---

## Installation Steps

### Step 1: Navigate to Project Directory

Open PowerShell and navigate to the project directory:

```powershell
cd c:\Users\IRM99K\ashwin\r2p
```

### Step 2: Run Setup Script

Execute the automated setup script:

```powershell
.\setup.ps1
```

This script will:
- Check Python installation
- Create a virtual environment
- Install all dependencies
- Create .env file from template

**OR Manual Setup:**

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Copy environment template
copy .env.example .env
```

---

## GitHub OAuth Setup

### Step 1: Create OAuth App

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Click **"New OAuth App"** button
3. Fill in the application details:

   ```
   Application name: Resume to Portfolio
   Homepage URL: http://localhost:5000
   Application description: Convert resumes to portfolio websites
   Authorization callback URL: http://localhost:5000/callback
   ```

4. Click **"Register application"**

### Step 2: Get Credentials

1. You'll see your **Client ID** on the next page - copy it
2. Click **"Generate a new client secret"**
3. Copy the **Client Secret** (you won't be able to see it again!)

### Step 3: Add to Environment Variables

Open `.env` file and add your credentials:

```
GITHUB_CLIENT_ID=your_client_id_here
GITHUB_CLIENT_SECRET=your_client_secret_here
GITHUB_REDIRECT_URI=http://localhost:5000/callback
```

---

## Perplexity API Setup

### Step 1: Create Perplexity Account

1. Go to [Perplexity AI](https://www.perplexity.ai/)
2. Sign up or log in

### Step 2: Get API Key

1. Navigate to [API Settings](https://www.perplexity.ai/settings/api)
2. Click **"Generate API Key"**
3. Copy your API key

### Step 3: Add to Environment Variables

Open `.env` file and add your API key:

```
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

### Step 4: Generate Secret Key

Generate a secure secret key for Flask:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Add it to `.env`:

```
SECRET_KEY=your_generated_secret_key_here
```

---

## Running the Application

### Option 1: Using Run Script (Recommended)

```powershell
.\run.ps1
```

### Option 2: Manual Start

```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Run the application
python app.py
```

### Expected Output

You should see:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

### Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

---

## Testing the Application

### Test 1: Login Flow

1. Click **"Sign in with GitHub"**
2. Authorize the application
3. You should be redirected to the upload page

### Test 2: Resume Upload

1. Prepare a test resume (PDF or DOCX)
2. Click the upload area or drag and drop your resume
3. Click **"Generate Portfolio"**
4. Wait for processing (may take 30-60 seconds)

### Test 3: Preview and Download

1. Click **"Preview Portfolio"** to see the generated HTML
2. Click **"Download HTML"** to save the file
3. Open the downloaded HTML file in a browser to verify

---

## Troubleshooting

### Problem: Python Not Found

**Solution:**
1. Install Python from [python.org](https://www.python.org/downloads/)
2. During installation, check "Add Python to PATH"
3. Restart PowerShell

### Problem: Virtual Environment Activation Error

**Error:** "cannot be loaded because running scripts is disabled"

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Problem: GitHub OAuth Not Working

**Symptoms:** Can't login or authentication fails

**Solutions:**
1. Verify Client ID and Secret in `.env` match your GitHub OAuth app
2. Check callback URL is exactly: `http://localhost:5000/callback`
3. Ensure your GitHub OAuth app is active
4. Clear browser cookies and try again

### Problem: Perplexity API Errors

**Symptoms:** Portfolio generation fails

**Solutions:**
1. Verify API key is correct in `.env`
2. Check your Perplexity account has available credits
3. Check API usage limits haven't been exceeded
4. Try with a shorter resume

### Problem: File Upload Fails

**Symptoms:** Error when uploading resume

**Solutions:**
1. Check file size is under 16MB
2. Ensure file format is PDF, DOC, or DOCX
3. Verify `uploads` directory exists and is writable
4. Try a different file

### Problem: PDF Parsing Issues

**Symptoms:** Can't extract text from PDF

**Solutions:**
```powershell
# Reinstall PDF libraries
pip uninstall PyPDF2 pdfplumber -y
pip install PyPDF2==3.0.1 pdfplumber==0.10.3
```

### Problem: Port 5000 Already in Use

**Solution:**
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

Or edit `app.py` and change the port:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Problem: Module Import Errors

**Solution:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Environment Variables Reference

Complete `.env` file template:

```
# Flask Configuration
SECRET_KEY=your-secret-key-here

# GitHub OAuth Configuration
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GITHUB_REDIRECT_URI=http://localhost:5000/callback

# Perplexity API Configuration
PERPLEXITY_API_KEY=your-perplexity-api-key
```

---

## Production Deployment

For production deployment, consider:

1. **Use a production WSGI server:**
   ```powershell
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set strong SECRET_KEY**
3. **Update GITHUB_REDIRECT_URI** to your production domain
4. **Enable HTTPS**
5. **Set environment to production:**
   ```python
   export FLASK_ENV=production
   ```

---

## Support

If you encounter issues not covered in this guide:

1. Check the [README.md](README.md) for additional information
2. Review error messages in the terminal
3. Check Flask logs for detailed error information
4. Verify all environment variables are set correctly

---

## Next Steps

Once the application is running successfully:

1. Test with different resume formats
2. Customize the HTML templates in `templates/` folder
3. Modify the portfolio generation prompt in `utils/portfolio_generator.py`
4. Add custom styling in `static/css/`

---

**Happy portfolio building! 🚀**
