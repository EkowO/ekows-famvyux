# File Organization Script for ekows-famvyux
# This script organizes all files into logical directories

Write-Host "🗂️ Organizing ekows-famvyux Project Files" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Ensure we're in the right directory
Set-Location "c:\Users\edakw\Downloads\fam\ekows-famvyux"

# Create directory structure
$directories = @(
    "scripts",
    "scripts\data_import", 
    "scripts\testing",
    "scripts\setup",
    "scripts\debugging",
    "scripts\utilities",
    "docs",
    "config"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "✅ Created directory: $dir" -ForegroundColor Green
    }
}

# Define file categories and their target directories
$fileCategories = @{
    # Data Import Scripts
    "scripts\data_import" = @(
        "add_movies.py",
        "add_popular_movies.py", 
        "download_imdb_csv.py",
        "import_csv_movies.py",
        "import_imdb_top1000.py",
        "update_comments_with_timestamps.py"
    )
    
    # Testing Files
    "scripts\testing" = @(
        "test_ai_manual.py",
        "test_ai_server.py", 
        "test_ai_styling.py",
        "test_ai_suggestions.py",
        "test_and_start_server.py",
        "test_chatbot_css.py",
        "test_css.html",
        "test_css_server.py",
        "test_environment.bat",
        "test_google_oauth.py",
        "test_imports.py",
        "test_oauth.py",
        "test_server.py",
        "minimal_test.py",
        "minimal_server_test.py",
        "complete_functionality_test.py"
    )
    
    # Setup Scripts
    "scripts\setup" = @(
        "setup_google_oauth.py",
        "setup_google_oauth_complete.py",
        "enable_google_oauth.py",
        "fix_css_and_start.ps1",
        "fix_css_and_start.bat"
    )
    
    # Debugging Scripts
    "scripts\debugging" = @(
        "debug_ai_bot.py",
        "debug_ai_error.py",
        "diagnose_css.py",
        "complete_ai_diagnosis.py",
        "comprehensive_diagnosis.py",
        "simple_ai_diagnosis.py",
        "simple_utils_test.py"
    )
    
    # Utility Scripts
    "scripts\utilities" = @(
        "start_ai_server.py",
        "start_debug_server.py", 
        "start_moviehub_ai.py",
        "start_server.py",
        "final_server.py",
        "quick_ai_test.py"
    )
    
    # Documentation
    "docs" = @(
        "AI_MOVIE_FEATURES.md",
        "AI_STYLING_UPDATE.md",
        "CSS_TROUBLESHOOTING.md", 
        "FIX_SUMMARY.md",
        "GOOGLE_OAUTH_SETUP.md",
        "GOOGLE_OAUTH_STATUS.md"
    )
    
    # Configuration
    "config" = @(
        "oauth_config.py"
    )
}

# Move files to their designated directories
foreach ($targetDir in $fileCategories.Keys) {
    Write-Host "`n📁 Moving files to $targetDir..." -ForegroundColor Yellow
    
    foreach ($file in $fileCategories[$targetDir]) {
        if (Test-Path $file) {
            try {
                Move-Item $file $targetDir -Force
                Write-Host "  ✅ Moved: $file" -ForegroundColor Green
            }
            catch {
                Write-Host "  ❌ Failed to move $file : $_" -ForegroundColor Red
            }
        }
        else {
            Write-Host "  ⚠️ File not found: $file" -ForegroundColor DarkYellow
        }
    }
}

# Handle special directories
Write-Host "`n📁 Organizing special directories..." -ForegroundColor Yellow

# Move 'get movies' directory if it exists
if (Test-Path "get movies") {
    if (!(Test-Path "data")) {
        New-Item -ItemType Directory -Path "data" -Force
    }
    Move-Item "get movies" "data\" -Force
    Write-Host "  ✅ Moved: 'get movies' folder to data/" -ForegroundColor Green
}

# Clean up cache
if (Test-Path "__pycache__") {
    Remove-Item "__pycache__" -Recurse -Force
    Write-Host "  🧹 Cleaned up __pycache__" -ForegroundColor Green
}

Write-Host "`n🎉 File organization complete!" -ForegroundColor Green
Write-Host "`n📋 Final project structure:" -ForegroundColor Cyan

# Display the organized structure
Get-ChildItem -Directory | ForEach-Object {
    Write-Host "📂 $($_.Name)/" -ForegroundColor Blue
    Get-ChildItem $_.FullName | ForEach-Object {
        if ($_.PSIsContainer) {
            Write-Host "  📂 $($_.Name)/" -ForegroundColor DarkBlue
        } else {
            Write-Host "  📄 $($_.Name)" -ForegroundColor Gray
        }
    }
}

Write-Host "`n✨ Core files remain in root:" -ForegroundColor Cyan
Get-ChildItem -File | Where-Object { $_.Name -match "\.(py|txt|md)$" } | ForEach-Object {
    Write-Host "  📄 $($_.Name)" -ForegroundColor White
}

Write-Host "`n💡 Next steps:" -ForegroundColor Magenta
Write-Host "  1. Update import paths in Python files if needed" -ForegroundColor White
Write-Host "  2. Update documentation references" -ForegroundColor White  
Write-Host "  3. Test the application: python main.py" -ForegroundColor White
