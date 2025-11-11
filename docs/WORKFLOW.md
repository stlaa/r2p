# User Workflow - Resume to Portfolio

## 📱 Complete User Journey

### Step 1: Landing Page
```
User opens: http://localhost:5000
↓
Automatically redirects to /login
```

**What user sees:**
- Clean login page with gradient background
- "Resume to Portfolio" branding
- "Sign in with GitHub" button (prominent)
- "Don't have a GitHub account?" section
- Link to create GitHub account
- Feature list (4 key features)

**User actions:**
- Clicks "Sign in with GitHub"

---

### Step 2: GitHub OAuth
```
Redirects to: https://github.com/login/oauth/authorize
↓
User logs in to GitHub (if not already)
↓
GitHub shows authorization screen
↓
User clicks "Authorize"
↓
GitHub redirects to: /callback?code=...
```

**What happens:**
- App exchanges code for access token
- App fetches user info from GitHub API
- App stores user in session
- App redirects to /upload

**User sees:**
- GitHub login screen (if needed)
- App authorization request
- Brief loading

---

### Step 3: Upload Page
```
User lands on: /upload
Session active with GitHub user info
```

**What user sees:**
- Header with:
  - User avatar
  - Username and display name
  - Logout button
- Upload area:
  - Large dashed box
  - "Click to upload or drag and drop"
  - "PDF or DOCX (Max 16MB)" hint
  - File icon
- Theme selector:
  - 4 theme cards in grid
  - Each showing 3 color dots
  - Theme name below
- "Generate Portfolio" button (disabled until file selected)

**User actions:**
1. Either:
   - Clicks upload area → file picker opens
   - Drags file and drops on upload area
2. Selects resume file (PDF or DOCX)
3. Sees confirmation: "✓ Selected: filename.pdf (2.3 MB)"
4. Selects a color theme (one is pre-selected)
5. Clicks "Generate Portfolio" button

---

### Step 4: Processing
```
AJAX POST to /generate with:
- resume file
- selected theme
```

**What user sees:**
- Form disappears
- Loading spinner appears
- Message: "Generating your portfolio... This may take a minute."

**What happens (backend):**
1. File saved to uploads/ folder
2. Resume parsed:
   - PDF → text extraction (PyPDF2)
   - DOCX → text extraction (python-docx)
3. Personal data filtered:
   - Phone numbers removed
   - Addresses removed
   - ZIP codes removed
4. Content sent to Perplexity API:
   - Structured prompt
   - Selected theme colors
   - Temperature 0.2 for consistency
5. HTML portfolio generated
6. Saved to generated/ folder
7. Uploaded file deleted
8. Portfolio info stored in session

**Timing:** 30-60 seconds

---

### Step 5: Result Page
```
User redirected to: /result
Session contains portfolio info
```

**What user sees:**
- Header with user info and buttons:
  - "Create New" button
  - "Logout" button
- Success icon: 🎉
- "Your Portfolio is Ready!"
- Portfolio info card:
  - Theme: "Professional Blue"
  - Status: "✓ Ready"
  - Format: "Single HTML File"
- Two large action buttons:
  - 👁️ Preview Portfolio
  - ⬇️ Download HTML
- "Create Another Portfolio" button
- Tips section:
  - Next steps listed
  - Deployment suggestions

**User actions:**
- Clicks "Preview Portfolio" → opens in new tab
- Clicks "Download HTML" → downloads file

---

### Step 6: Preview
```
User clicks "Preview Portfolio"
Opens: /preview/<filename> in new tab
```

**What user sees:**
- Complete portfolio website
- Selected color theme applied
- All resume content formatted:
  - Header with name and title
  - Professional summary
  - Work experience
  - Education
  - Skills
  - Projects (if available)
  - Certifications (if available)
- Responsive design
- Professional styling
- No personal data (phone/address)

**User actions:**
- Reviews portfolio
- Closes tab if satisfied

---

### Step 7: Download
```
User clicks "Download HTML"
Triggers: /download/<filename>
```

**What happens:**
- Browser downloads file: "portfolio.html"
- File is complete, self-contained HTML
- Can be opened in any browser
- Can be uploaded to any hosting

**User actions:**
- Saves file to computer
- Can open locally to verify
- Can upload to hosting service

---

### Step 8: Next Actions

**Option A: Create Another**
- Clicks "Create Another Portfolio"
- Returns to /upload
- Can upload different resume or try different theme

**Option B: Logout**
- Clicks "Logout"
- Session cleared
- Returns to /login

**Option C: Close Browser**
- Session remains active
- Can return to /upload later
- Session expires after browser closes

---

## 🎯 Key User Touchpoints

### 1. Login Page
**First impression matters**
- Professional design
- Clear call-to-action
- Feature highlights
- Easy GitHub signup link

### 2. Upload Page
**Simple and intuitive**
- Clear upload area
- Visual theme preview
- Immediate file feedback
- One-click generation

### 3. Processing
**Managing expectations**
- Clear loading state
- Time expectation set
- No confusion about status

### 4. Result Page
**Success celebration**
- Positive reinforcement
- Clear next actions
- Multiple options
- Helpful guidance

### 5. Preview
**The payoff**
- Beautiful portfolio
- Professional appearance
- Content well-formatted
- Mobile-responsive

---

## ⚡ Quick Path (Optimal Flow)

```
Login (5 sec)
    ↓
Upload resume (10 sec)
    ↓
Select theme (5 sec)
    ↓
Click generate (1 sec)
    ↓
Wait for generation (45 sec)
    ↓
Preview & download (10 sec)
    ↓
Total: ~76 seconds
```

---

## 🔄 Alternative Flows

### Flow 1: Multiple Attempts
```
Login → Upload → Generate → Preview → Not satisfied
    ↓
Create new → Upload → Try different theme → Generate → Preview → Satisfied
    ↓
Download → Done
```

### Flow 2: Batch Creation
```
Login → Upload Resume A → Theme 1 → Generate → Download
    ↓
Create new → Upload Resume B → Theme 2 → Generate → Download
    ↓
Create new → Upload Resume A → Theme 3 → Generate → Download
    ↓
Logout
```

### Flow 3: Preview Only
```
Login → Upload → Generate → Preview → Close
    ↓
(Downloads later from Result page)
```

---

## 🛡️ Error Handling Paths

### Scenario 1: Invalid File
```
User uploads .txt file
    ↓
Error shown: "Invalid file format. Please upload PDF or DOCX file."
    ↓
User can try again immediately
```

### Scenario 2: OAuth Fails
```
GitHub auth fails
    ↓
Redirect to login with error message
    ↓
User can try again
```

### Scenario 3: API Failure
```
Perplexity API fails
    ↓
Error message shown
    ↓
Form reappears
    ↓
User can try again
```

### Scenario 4: Empty Resume
```
Resume has no extractable text
    ↓
Error: "Unable to extract content from resume."
    ↓
User tries different file
```

---

## 💡 User Experience Details

### Visual Feedback
- ✓ File selection confirmation
- ✓ Theme selection highlight
- ✓ Button hover effects
- ✓ Loading spinner during processing
- ✓ Success icon on completion
- ✓ Error messages when needed

### Intuitive Design
- Upload area looks clickable
- Drag-and-drop area clearly marked
- Theme cards show visual preview
- Buttons clearly labeled
- Progress indicators present
- Back navigation available

### Error Prevention
- File type validation
- File size limits
- Required field enforcement
- Session validation
- API error handling

### Responsive Design
- Works on mobile phones
- Optimized for tablets
- Enhanced on desktop
- Touch-friendly
- Keyboard accessible

---

## 📊 Expected Outcomes

### Successful Generation
**User gets:**
- Professional portfolio website
- Single HTML file
- Chosen color theme applied
- All resume content included
- No personal data exposed
- Mobile-responsive design
- Ready to host immediately

### Quality Indicators
**User sees:**
- Clean, modern design
- Proper formatting
- Organized sections
- Professional typography
- Consistent colors
- Smooth animations
- Print-friendly layout

---

## 🎉 Success State

**User has achieved:**
- ✅ Created portfolio in under 2 minutes
- ✅ No technical knowledge required
- ✅ Professional-looking result
- ✅ Downloadable, hostable file
- ✅ Privacy maintained
- ✅ Multiple theme options tried
- ✅ Shareable portfolio ready

**User can now:**
- Upload to GitHub Pages
- Share with employers
- Add to LinkedIn
- Use as personal website
- Print as formatted resume
- Update anytime by regenerating

---

**The entire process is designed for simplicity, speed, and professional results!** 🚀
