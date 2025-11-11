# Run the Flask application
Write-Host "Starting Resume to Portfolio application..." -ForegroundColor Cyan
Write-Host "The application will be available at http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Activate virtual environment if not already activated
if (-not $env:VIRTUAL_ENV) {
    & ".\venv\Scripts\Activate.ps1"
}

# Run the Flask app
python app.py
