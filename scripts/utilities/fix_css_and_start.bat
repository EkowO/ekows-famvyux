@echo off
echo 🔧 Fixing AI Chatbot CSS Issues
echo ================================

echo.
echo 📁 Checking file structure...
if not exist "static\styles.css" (
    echo ❌ Error: static\styles.css not found!
    pause
    exit /b 1
)
echo ✅ CSS file found

if not exist "templates\browse_movies.html" (
    echo ❌ Error: templates\browse_movies.html not found!
    pause
    exit /b 1
)
echo ✅ Template file found

echo.
echo 🧹 Clearing potential cache issues...
:: Clear any Python cache
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "app\__pycache__" rmdir /s /q "app\__pycache__"

echo.
echo 🚀 Starting server with debug info...
echo    Server will start at: http://localhost:8000
echo    Browse page: http://localhost:8000/browse
echo    CSS test page: http://localhost:8000/test-css (if using test server)
echo.
echo 💡 If CSS still doesn't work:
echo    1. Press Ctrl+F5 in browser to force refresh
echo    2. Open Dev Tools (F12) and check Network tab
echo    3. Look for styles.css request - should be 200 OK
echo    4. Check Console tab for any errors
echo.

:: Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
