#!/usr/bin/env python3
"""
Comprehensive file organization script for ekows-famvyux project
This script will organize all files into a clean, logical structure
"""

import os
import shutil
from pathlib import Path

def organize_project():
    """Organize all project files into logical directories"""
    
    print("🗂️ Organizing ekows-famvyux Project Files")
    print("=" * 50)
    
    # Get project root
    project_root = Path.cwd()
    print(f"📁 Working in: {project_root}")
    
    # Define directory structure
    directories = {
        'scripts': {
            'data_import': [],
            'testing': [], 
            'setup': [],
            'debugging': [],
            'utilities': []
        },
        'docs': [],
        'config': [],
        'data': []
    }
    
    # Create directories
    for main_dir, subdirs in directories.items():
        main_path = project_root / main_dir
        main_path.mkdir(exist_ok=True)
        print(f"✅ Created: {main_dir}/")
        
        if isinstance(subdirs, dict):
            for subdir in subdirs.keys():
                sub_path = main_path / subdir
                sub_path.mkdir(exist_ok=True)
                print(f"  ✅ Created: {main_dir}/{subdir}/")
    
    # Define file mappings
    file_mappings = {
        # Data import scripts
        'scripts/data_import': [
            'add_movies.py',
            'add_popular_movies.py', 
            'download_imdb_csv.py',
            'import_csv_movies.py',
            'import_imdb_top1000.py',
            'update_comments_with_timestamps.py'
        ],
        
        # Testing files  
        'scripts/testing': [
            'test_ai_manual.py',
            'test_ai_server.py',
            'test_ai_styling.py', 
            'test_ai_suggestions.py',
            'test_and_start_server.py',
            'test_chatbot_css.py',
            'test_css.html',
            'test_css_server.py',
            'test_environment.bat',
            'test_google_oauth.py',
            'test_imports.py',
            'test_oauth.py',
            'test_server.py',
            'minimal_test.py',
            'minimal_server_test.py',
            'complete_functionality_test.py'
        ],
        
        # Setup scripts
        'scripts/setup': [
            'setup_google_oauth.py',
            'setup_google_oauth_complete.py',
            'enable_google_oauth.py',
            'fix_css_and_start.ps1',
            'fix_css_and_start.bat'
        ],
        
        # Debugging scripts
        'scripts/debugging': [
            'debug_ai_bot.py',
            'debug_ai_error.py',
            'diagnose_css.py',
            'complete_ai_diagnosis.py',
            'comprehensive_diagnosis.py', 
            'simple_ai_diagnosis.py',
            'simple_utils_test.py'
        ],
        
        # Utility scripts
        'scripts/utilities': [
            'start_ai_server.py',
            'start_debug_server.py',
            'start_moviehub_ai.py', 
            'start_server.py',
            'final_server.py',
            'quick_ai_test.py'
        ],
        
        # Documentation
        'docs': [
            'AI_MOVIE_FEATURES.md',
            'AI_STYLING_UPDATE.md',
            'CSS_TROUBLESHOOTING.md',
            'FIX_SUMMARY.md', 
            'GOOGLE_OAUTH_SETUP.md',
            'GOOGLE_OAUTH_STATUS.md'
        ],
        
        # Configuration
        'config': [
            'oauth_config.py'
        ]
    }
    
    # Move files
    moved_count = 0
    for target_dir, files in file_mappings.items():
        print(f"\n📁 Moving files to {target_dir}...")
        target_path = project_root / target_dir
        
        for filename in files:
            source_path = project_root / filename
            if source_path.exists():
                try:
                    shutil.move(str(source_path), str(target_path / filename))
                    print(f"  ✅ Moved: {filename}")
                    moved_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to move {filename}: {e}")
            else:
                print(f"  ⚠️ File not found: {filename}")
    
    # Handle special directories
    print(f"\n📁 Organizing special directories...")
    
    # Move 'get movies' directory
    get_movies_path = project_root / "get movies"
    if get_movies_path.exists():
        data_path = project_root / "data"
        data_path.mkdir(exist_ok=True)
        try:
            shutil.move(str(get_movies_path), str(data_path / "get movies"))
            print(f"  ✅ Moved: 'get movies' folder to data/")
            moved_count += 1
        except Exception as e:
            print(f"  ❌ Failed to move 'get movies': {e}")
    
    # Clean up cache
    pycache_path = project_root / "__pycache__"
    if pycache_path.exists():
        try:
            shutil.rmtree(pycache_path)
            print(f"  🧹 Cleaned up __pycache__")
        except Exception as e:
            print(f"  ❌ Failed to clean __pycache__: {e}")
    
    print(f"\n🎉 File organization complete!")
    print(f"📊 Moved {moved_count} files/directories")
    
    # Display final structure
    print(f"\n📋 Final project structure:")
    display_tree(project_root, max_depth=2)
    
    print(f"\n✨ Core files remaining in root:")
    for item in project_root.iterdir():
        if item.is_file() and item.suffix in ['.py', '.txt', '.md']:
            print(f"  📄 {item.name}")
    
    print(f"\n💡 Next steps:")
    print(f"  1. Update any import paths in scripts if needed")
    print(f"  2. Update documentation references") 
    print(f"  3. Test the application: python main.py")

def display_tree(path, prefix="", max_depth=3, current_depth=0):
    """Display directory tree structure"""
    if current_depth >= max_depth:
        return
        
    items = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
    
    for i, item in enumerate(items):
        is_last = i == len(items) - 1
        current_prefix = "└── " if is_last else "├── "
        
        if item.is_dir():
            print(f"{prefix}{current_prefix}📂 {item.name}/")
            extension = "    " if is_last else "│   "
            display_tree(item, prefix + extension, max_depth, current_depth + 1)
        else:
            icon = "📄" if item.suffix in ['.py', '.md', '.txt', '.html'] else "📄"
            print(f"{prefix}{current_prefix}{icon} {item.name}")

if __name__ == "__main__":
    organize_project()
