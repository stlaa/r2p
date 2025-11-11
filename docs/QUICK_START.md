# Quick Start Guide - Resume to Portfolio

## ✅ Pre-Flight Checklist

Run this command to validate your setup:
```bash
python test_setup.py
```

All tests should pass before proceeding.

## 🚀 Starting the Application

### Option 1: Direct Python
```bash
python app.py
```

### Option 2: PowerShell Script
```powershell
.\run.ps1
```

The application will start on **http://localhost:5000**

## 📝 First-Time Setup

### 1. Create GitHub OAuth App

1. Go to: https://github.com/settings/developers
2. Click **"New OAuth App"**
3. Fill in:
   - **Application name**: Resume to Portfolio (or your choice)
   - **Homepage URL**: `http://localhost:5000`
   - **Authorization callback URL**: `http://localhost:5000/callback`
4. Click **"Register application"**
5. Copy **Client ID** and **Client Secret**
6. Add them to your `.env` file

### 2. Get Perplexity API Key

1. Sign up at: https://www.perplexity.ai/
2. Go to: https://www.perplexity.ai/settings/api
3. Click **"Generate API Key"**
4. Copy the key
5. Add it to your `.env` file

### 3. Generate Secret Key

Run this command:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and add it to your `.env` file as `SECRET_KEY`

## 🎯 Testing the Complete Workflow

### Test Flow:

1. **Start the app**: `python app.py`
2. **Open browser**: http://localhost:5000
3. **Test Login**:
   - Click "Sign in with GitHub"
   - Authorize the app
   - Should redirect to upload page
4. **Test Upload**:
   - Click the upload area
   - Select a PDF or DOCX resume
   - Choose a color theme
   - Click "Generate Portfolio"
5. **Wait for Generation**:
   - Should take 30-60 seconds
   - Loading spinner will show
6. **Test Result Page**:
   - Should see success message
   - Click "Preview Portfolio" - opens in new tab
   - Click "Download HTML" - downloads file
7. **Test Logout**:
   - Click "Logout"
   - Should return to login page

## 🧪 Test Resume

If you don't have a resume ready, create a simple test one:

**test_resume.txt** (save as PDF):
```
John Doe
Software Engineer

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years in web development.

WORK EXPERIENCE

Senior Developer | Tech Corp | 2020-Present
- Built scalable web applications
- Led team of 5 developers
- Improved performance by 40%

Junior Developer | StartUp Inc | 2018-2020
- Developed REST APIs
- Worked with React and Node.js

EDUCATION

Bachelor of Science in Computer Science
University of Technology | 2014-2018

SKILLS

Programming: Python, JavaScript, Java, C++
Web: React, Node.js, Flask, Django
Database: PostgreSQL, MongoDB
Tools: Git, Docker, AWS

PROJECTS

E-Commerce Platform
- Built full-stack application
- Integrated payment gateway
- 10,000+ active users

CERTIFICATIONS

AWS Certified Developer
Google Cloud Professional
```

Convert this to PDF using Word or any PDF converter.

## 🎨 Testing Each Theme

Test all 4 color themes to see the variety:

1. **Professional Blue** - Classic corporate look
2. **Elegant Purple** - Creative and modern
3. **Modern Green** - Fresh and energetic
4. **Classic Gray** - Minimalist and clean

## ✓ Success Indicators

You'll know everything works when:

- [x] Login redirects properly after GitHub auth
- [x] File upload shows selected filename
- [x] Generation completes without errors
- [x] Preview opens in new tab and looks professional
- [x] Download saves a complete HTML file
- [x] HTML file opens correctly in any browser
- [x] Portfolio is mobile-responsive
- [x] Personal data (phone/address) is not visible in preview

## ❌ Common Issues

### Issue: "Configuration Error"
**Solution**: Check your `.env` file has all three required keys

### Issue: GitHub login redirects to error page
**Solution**: 
- Verify callback URL in GitHub app settings
- Must be exactly: `http://localhost:5000/callback`

### Issue: "Failed to generate portfolio"
**Solution**:
- Check Perplexity API key is valid
- Verify you have API credits remaining
- Check internet connection

### Issue: Upload fails
**Solution**:
- Ensure file is PDF or DOCX (not DOC)
- Check file size < 16MB
- Make sure file is not password-protected

### Issue: Can't extract content
**Solution**:
- PDF must have selectable text (not scanned image)
- Try converting to DOCX format
- Ensure proper encoding

## 🔧 Debug Mode

The app runs in debug mode by default (`debug=True` in app.py).

This provides:
- Detailed error messages
- Auto-reload on code changes
- Better stack traces

For production, set `debug=False`.

## 📊 Monitoring

Check these during testing:

1. **Terminal Output**: Watch for errors or warnings
2. **Browser Console**: Check for JavaScript errors (F12)
3. **Network Tab**: Monitor API calls (F12 → Network)
4. **Generated Files**: Check `generated/` folder for HTML files

## 🎉 Next Steps After Testing

Once everything works:

1. **Deploy** to a production server (optional)
2. **Share** the application with others
3. **Customize** themes in `config.py`
4. **Modify** portfolio structure in `portfolio_generator.py`
5. **Add features** like more themes or export formats

## 📞 Support

If you encounter issues:

1. Run `python test_setup.py` to diagnose
2. Check error messages in terminal
3. Review the README.md for detailed docs
4. Check `.env` file configuration

## 🎯 Performance Benchmarks

Expected timings:
- Login flow: < 5 seconds
- Resume parsing: < 2 seconds
- Portfolio generation: 30-60 seconds (API call)
- Preview load: < 1 second
- Download: Instant

---

**You're all set! Happy portfolio creating! 🚀**
