# GitHub Pages Deployment Feature

## Overview
This feature allows users to deploy their generated portfolio HTML directly to GitHub Pages with a single click from the result page.

## Implementation Details

### 1. Updated OAuth Scope
- Modified the GitHub OAuth flow to request `repo` permission in addition to `user:email`
- This allows the app to create repositories and push files on behalf of the user
- **Location**: `app.py` - `github_auth()` route

### 2. Added Dependencies
- Added `PyGithub==2.1.1` to `requirements.txt` for GitHub API interactions
- **Installation**: Run `pip install -r requirements.txt` to install the new dependency

### 3. Configuration Updates
- Added `GITHUB_REPOS_API_URL` constant to `config.py` for GitHub repository API endpoint

### 4. Deploy Endpoint
- Added new POST route `/deploy/<filename>` in `app.py`
- **Functionality**:
  - Authenticates the user
  - Reads the generated portfolio HTML
  - Creates or updates the user's `<username>.github.io` repository
  - Pushes the portfolio as `index.html` to the repository
  - Enables GitHub Pages on the `main` branch
  - Returns the live URL and deployment status

### 5. UI Updates in result.html
- Added "Deploy to GitHub Pages" button with gradient styling
- Added deployment status area that shows:
  - Loading state with spinner during deployment
  - Success message with live portfolio URL
  - Error messages if deployment fails
- Added JavaScript to handle the deploy button click event:
  - Makes POST request to `/deploy/<filename>`
  - Updates UI based on deployment status
  - Disables button during deployment

## How It Works

1. **User generates portfolio**: After uploading resume and selecting theme
2. **Result page displays**: Shows preview, download, and deploy options
3. **User clicks "Deploy to GitHub Pages"**:
   - Button shows loading state
   - App checks if `<username>.github.io` repository exists
   - If not, creates the repository
   - Creates or updates `index.html` with portfolio content
   - Enables GitHub Pages
   - Returns live URL to user
4. **Success**: User sees their portfolio URL (https://username.github.io)
5. **Note**: GitHub Pages may take a few minutes to propagate changes

## Required Permissions

When users log in, they will now be asked to grant:
- **user:email**: Read user email address
- **repo**: Full control of private and public repositories (needed to create repos and push files)

## Repository Structure

The deployed repository will have:
- `main` branch (default)
- `index.html` (the portfolio)
- GitHub Pages enabled, serving from `main` branch

## Error Handling

The deployment endpoint handles:
- Authentication errors
- File not found errors
- GitHub API errors (rate limits, permissions, etc.)
- Repository creation/update failures

## Future Enhancements

Possible improvements:
- Custom domain support
- Deploy to a subdirectory instead of root
- Version history/rollback
- Custom repository names
- Preview before deploy
- Analytics integration
