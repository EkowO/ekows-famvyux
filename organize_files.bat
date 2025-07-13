@echo off
echo 🗂️ Organizing ekows-famvyux Project Files
echo =========================================

:: Create directory structure
echo 📁 Creating directory structure...
mkdir scripts 2>nul
mkdir scripts\data_import 2>nul
mkdir scripts\testing 2>nul
mkdir scripts\setup 2>nul
mkdir scripts\debugging 2>nul
mkdir scripts\utilities 2>nul
mkdir docs 2>nul
mkdir config 2>nul
mkdir data 2>nul

:: Move data import files
echo 📁 Moving data import files...
move add_movies.py scripts\data_import\ 2>nul
move add_popular_movies.py scripts\data_import\ 2>nul
move download_imdb_csv.py scripts\data_import\ 2>nul
move import_csv_movies.py scripts\data_import\ 2>nul
move import_imdb_top1000.py scripts\data_import\ 2>nul
move update_comments_with_timestamps.py scripts\data_import\ 2>nul

:: Move testing files
echo 📁 Moving testing files...
move test_ai_manual.py scripts\testing\ 2>nul
move test_ai_server.py scripts\testing\ 2>nul
move test_ai_styling.py scripts\testing\ 2>nul
move test_ai_suggestions.py scripts\testing\ 2>nul
move test_and_start_server.py scripts\testing\ 2>nul
move test_chatbot_css.py scripts\testing\ 2>nul
move test_css.html scripts\testing\ 2>nul
move test_css_server.py scripts\testing\ 2>nul
move test_environment.bat scripts\testing\ 2>nul
move test_google_oauth.py scripts\testing\ 2>nul
move test_imports.py scripts\testing\ 2>nul
move test_oauth.py scripts\testing\ 2>nul
move test_server.py scripts\testing\ 2>nul
move minimal_test.py scripts\testing\ 2>nul
move minimal_server_test.py scripts\testing\ 2>nul
move complete_functionality_test.py scripts\testing\ 2>nul

:: Move setup files
echo 📁 Moving setup files...
move setup_google_oauth.py scripts\setup\ 2>nul
move setup_google_oauth_complete.py scripts\setup\ 2>nul
move enable_google_oauth.py scripts\setup\ 2>nul
move fix_css_and_start.ps1 scripts\setup\ 2>nul
move fix_css_and_start.bat scripts\setup\ 2>nul

:: Move debugging files  
echo 📁 Moving debugging files...
move debug_ai_bot.py scripts\debugging\ 2>nul
move debug_ai_error.py scripts\debugging\ 2>nul
move diagnose_css.py scripts\debugging\ 2>nul
move complete_ai_diagnosis.py scripts\debugging\ 2>nul
move comprehensive_diagnosis.py scripts\debugging\ 2>nul
move simple_ai_diagnosis.py scripts\debugging\ 2>nul
move simple_utils_test.py scripts\debugging\ 2>nul

:: Move utility files
echo 📁 Moving utility files...
move start_ai_server.py scripts\utilities\ 2>nul
move start_debug_server.py scripts\utilities\ 2>nul
move start_moviehub_ai.py scripts\utilities\ 2>nul
move start_server.py scripts\utilities\ 2>nul
move final_server.py scripts\utilities\ 2>nul
move quick_ai_test.py scripts\utilities\ 2>nul

:: Move documentation files
echo 📁 Moving documentation files...
move AI_MOVIE_FEATURES.md docs\ 2>nul
move AI_STYLING_UPDATE.md docs\ 2>nul
move CSS_TROUBLESHOOTING.md docs\ 2>nul
move FIX_SUMMARY.md docs\ 2>nul
move GOOGLE_OAUTH_SETUP.md docs\ 2>nul
move GOOGLE_OAUTH_STATUS.md docs\ 2>nul

:: Move configuration files
echo 📁 Moving configuration files...
move oauth_config.py config\ 2>nul

:: Move data folders
echo 📁 Moving data folders...
move "get movies" data\ 2>nul

:: Clean up cache
echo 🧹 Cleaning up cache...
rmdir /s /q __pycache__ 2>nul

echo.
echo 🎉 File organization complete!
echo.
echo 📋 Organized structure:
echo   📂 app/ - Core application code
echo   📂 config/ - Configuration files
echo   📂 data/ - Data files and imports
echo   📂 docs/ - Documentation
echo   📂 scripts/ - All utility scripts organized by category
echo   📂 static/ - Web assets (CSS, JS, images)
echo   📂 templates/ - HTML templates
echo   📄 main.py - Main application entry point
echo   📄 requirements.txt - Python dependencies
echo.
echo ✨ Core application files remain in root directory
echo 💡 All helper scripts are now organized in the scripts/ folder

pause
