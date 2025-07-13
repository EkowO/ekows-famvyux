# AI Chatbot CSS Fix Script
Write-Host "🔧 Fixing AI Chatbot CSS Issues" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check file structure
Write-Host "📁 Checking file structure..." -ForegroundColor Yellow
if (-not (Test-Path "static\styles.css")) {
    Write-Host "❌ Error: static\styles.css not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ CSS file found" -ForegroundColor Green

if (-not (Test-Path "templates\browse_movies.html")) {
    Write-Host "❌ Error: templates\browse_movies.html not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Template file found" -ForegroundColor Green

Write-Host ""
Write-Host "🧹 Clearing potential cache issues..." -ForegroundColor Yellow
# Clear Python cache
if (Test-Path "__pycache__") {
    Remove-Item -Recurse -Force "__pycache__"
}
if (Test-Path "app\__pycache__") {
    Remove-Item -Recurse -Force "app\__pycache__"
}

Write-Host ""
Write-Host "🚀 Starting server with debug info..." -ForegroundColor Green
Write-Host "   Server will start at: http://localhost:8000" -ForegroundColor White
Write-Host "   Browse page: http://localhost:8000/browse" -ForegroundColor White
Write-Host ""
Write-Host "💡 If CSS still doesn't work:" -ForegroundColor Magenta
Write-Host "   1. Press Ctrl+F5 in browser to force refresh" -ForegroundColor White
Write-Host "   2. Open Dev Tools (F12) and check Network tab" -ForegroundColor White
Write-Host "   3. Look for styles.css request - should be 200 OK" -ForegroundColor White
Write-Host "   4. Check Console tab for any errors" -ForegroundColor White
Write-Host ""

# Start the server
try {
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
} catch {
    Write-Host "❌ Error starting server: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔍 Try these troubleshooting steps:" -ForegroundColor Yellow
    Write-Host "1. Check if Python is installed: python --version" -ForegroundColor White
    Write-Host "2. Check if uvicorn is installed: pip show uvicorn" -ForegroundColor White
    Write-Host "3. Install requirements: pip install -r requirements.txt" -ForegroundColor White
}

Read-Host "Press Enter to exit"
