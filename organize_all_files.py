#!/usr/bin/env python3
"""
Comprehensive File Organization Script for MovieHub Project
Organizes all files into logical directory structure
"""

import os
import shutil
from pathlib import Path

# Base directory (current project directory)
BASE_DIR = Path(__file__).parent

# Directory structure definition
DIRECTORIES = {
    # Core application directories (already organized)
    'app': 'Core application code and routes',
    'static': 'Static files (CSS, JS, images)',
    'templates': 'HTML templates',
    
    # Data and configuration
    'data': 'Data files and databases',
    'config': 'Configuration files and OAuth setup',
    
    # Scripts organized by purpose
    'scripts': {
        'data_import': 'Scripts for importing movie data',
        'setup': 'Setup and configuration scripts',
        'testing': 'Testing and debugging scripts',
        'utilities': 'Utility scripts and helpers',
        'server': 'Server startup scripts'
    },
    
    # Documentation
    'docs': {
        'setup': 'Setup and installation guides',
        'features': 'Feature documentation',
        'troubleshooting': 'Troubleshooting guides',
        'api': 'API documentation'
    },
    
    # Development and testing
    'tests': 'Test files',
    'tools': 'Development tools and utilities',
    
    # Archive for old files
    'archive': 'Archived and deprecated files'
}

# File organization mapping
FILE_MAPPINGS = {
    # Data import scripts
    'scripts/data_import': [
        'add_movies.py',
        'add_popular_movies.py',
        'download_imdb_csv.py',
        'import_csv_movies.py',
        'import_imdb_top1000.py',
        'update_comments_with_timestamps.py'
    ],
    
    # Setup scripts
    'scripts/setup': [
        'setup_google_oauth.py',
        'setup_google_oauth_complete.py',
        'enable_google_oauth.py',
        'oauth_config.py'
    ],
    
    # Testing scripts
    'scripts/testing': [
        'test_ai_manual.py',
        'test_ai_server.py',
        'test_ai_styling.py',
        'test_ai_suggestions.py',
        'test_chatbot_css.py',
        'test_css_server.py',
        'test_google_oauth.py',
        'test_imports.py',
        'test_oauth.py',
        'test_server.py',
        'complete_functionality_test.py',
        'minimal_test.py',
        'minimal_server_test.py',
        'simple_utils_test.py'
    ],
    
    # Server scripts
    'scripts/server': [
        'start_ai_server.py',
        'start_debug_server.py',
        'start_moviehub_ai.py',
        'start_server.py',
        'test_and_start_server.py',
        'final_server.py'
    ],
    
    # Utility scripts
    'scripts/utilities': [
        'organize_project.py',
        'organize_files.bat',
        'organize_files.ps1',
        'fix_css_and_start.bat',
        'fix_css_and_start.ps1',
        'test_environment.bat'
    ],
    
    # Debugging scripts
    'scripts/debugging': [
        'debug_ai_bot.py',
        'debug_ai_error.py',
        'diagnose_css.py',
        'comprehensive_diagnosis.py',
        'complete_ai_diagnosis.py',
        'simple_ai_diagnosis.py',
        'quick_ai_test.py'
    ],
    
    # Documentation files
    'docs/features': [
        'AI_MOVIE_FEATURES.md',
        'AI_STYLING_UPDATE.md'
    ],
    
    'docs/setup': [
        'GOOGLE_OAUTH_SETUP.md',
        'GOOGLE_OAUTH_STATUS.md'
    ],
    
    'docs/troubleshooting': [
        'CSS_TROUBLESHOOTING.md',
        'FIX_SUMMARY.md',
        'FILTER_CSS_IMPROVEMENTS.md'
    ],
    
    # Test files
    'tests': [
        'test_css.html',
        'test_filter_layout.html'
    ],
    
    # Data files
    'data': [
        'get movies/'  # This is a directory
    ],
    
    # Static files cleanup
    'archive': [
        'static/styles_new.css'  # Archive old CSS file
    ]
}

def create_directories():
    """Create the directory structure"""
    print("📁 Creating directory structure...")
    
    def create_dir(path, description=""):
        full_path = BASE_DIR / path
        full_path.mkdir(parents=True, exist_ok=True)
        if description:
            # Create a README.md file with description
            readme_path = full_path / "README.md"
            if not readme_path.exists():
                with open(readme_path, 'w') as f:
                    f.write(f"# {path.split('/')[-1].replace('_', ' ').title()}\n\n{description}\n")
        print(f"  ✓ Created: {path}")
    
    # Create main directories
    for dir_name, description in DIRECTORIES.items():
        if isinstance(description, dict):
            # Handle nested directories
            for sub_dir, sub_desc in description.items():
                create_dir(f"{dir_name}/{sub_dir}", sub_desc)
        else:
            create_dir(dir_name, description)

def move_files():
    """Move files to their appropriate directories"""
    print("\n📦 Moving files to organized structure...")
    
    moved_count = 0
    
    for target_dir, files in FILE_MAPPINGS.items():
        target_path = BASE_DIR / target_dir
        
        for file_item in files:
            source_path = BASE_DIR / file_item
            
            if source_path.exists():
                if source_path.is_dir():
                    # Handle directory moves
                    target_file_path = target_path / source_path.name
                    if not target_file_path.exists():
                        shutil.move(str(source_path), str(target_file_path))
                        print(f"  ✓ Moved directory: {file_item} → {target_dir}/")
                        moved_count += 1
                else:
                    # Handle file moves
                    target_file_path = target_path / source_path.name
                    if not target_file_path.exists():
                        shutil.move(str(source_path), str(target_file_path))
                        print(f"  ✓ Moved: {file_item} → {target_dir}/")
                        moved_count += 1
            else:
                print(f"  ⚠️  File not found: {file_item}")
    
    print(f"\n📈 Total files moved: {moved_count}")

def create_documentation():
    """Create comprehensive documentation files"""
    print("\n📝 Creating documentation...")
    
    # Main README update
    readme_content = """# MovieHub - IMDB-Style Movie Database

A modern, responsive movie database application with AI-powered recommendations and comprehensive movie management features.

## 🎬 Features

- **Movie Database**: Browse, search, and discover movies
- **AI Recommendations**: Intelligent movie suggestions based on preferences
- **User Management**: User accounts with Google OAuth integration
- **Responsive Design**: IMDB-inspired dark theme with mobile support
- **Advanced Filtering**: Multi-column responsive filter system
- **Comments System**: User reviews and ratings
- **Watch Later**: Personal movie watchlist management

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**:
   ```bash
   python main.py
   ```

3. **Access the Application**:
   Open your browser to `http://localhost:8000`

## 📁 Project Structure

```
ekows-famvyux/
├── app/                    # Core application code
├── static/                 # CSS, JS, and static assets
├── templates/              # HTML templates
├── scripts/                # Organized scripts by purpose
│   ├── data_import/        # Data import and management
│   ├── setup/              # Configuration and setup
│   ├── testing/            # Testing and debugging
│   ├── server/             # Server startup scripts
│   └── utilities/          # Helper scripts
├── docs/                   # Documentation
├── data/                   # Data files and databases
├── config/                 # Configuration files
└── tests/                  # Test files
```

## 🔧 Configuration

- **Database**: SQLite database for movie storage
- **Authentication**: Google OAuth integration
- **AI Features**: OpenAI integration for recommendations

## 📚 Documentation

- [Setup Guide](docs/setup/)
- [Feature Documentation](docs/features/)
- [Troubleshooting](docs/troubleshooting/)

## 🛠️ Development

- **Framework**: FastAPI
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLite
- **Authentication**: Google OAuth
- **AI**: OpenAI GPT integration

## 📄 License

This project is licensed under the MIT License.
"""
    
    with open(BASE_DIR / "README.md", 'w') as f:
        f.write(readme_content)
    
    # Project structure documentation
    structure_doc = """# Project Structure Guide

## Directory Organization

### Core Application (`app/`)
- `config.py` - Application configuration
- `routes_*.py` - API route handlers
- `utils.py` - Utility functions

### Frontend (`static/` & `templates/`)
- `static/styles.css` - Main CSS file with MovieHub theme
- `templates/` - Jinja2 HTML templates

### Scripts (`scripts/`)
Organized by purpose:

#### Data Import (`scripts/data_import/`)
- Movie data importing and management
- CSV processing scripts
- Database update utilities

#### Setup (`scripts/setup/`)
- OAuth configuration
- Environment setup
- Initial project configuration

#### Testing (`scripts/testing/`)
- Unit tests and integration tests
- Manual testing scripts
- Debug utilities

#### Server (`scripts/server/`)
- Server startup scripts
- Production deployment helpers

#### Utilities (`scripts/utilities/`)
- File organization tools
- Development helpers
- Batch processing scripts

### Documentation (`docs/`)
- Setup guides and installation instructions
- Feature documentation
- Troubleshooting guides
- API documentation

### Data (`data/`)
- Movie databases
- Imported data files
- User data storage

## File Naming Conventions

- **Scripts**: Use descriptive names with underscores
- **Documentation**: Use UPPERCASE for markdown files
- **Templates**: Use lowercase with underscores
- **Static files**: Use lowercase with hyphens for CSS classes

## Development Workflow

1. Make changes in appropriate directories
2. Test using scripts in `scripts/testing/`
3. Update documentation in `docs/`
4. Use utility scripts for maintenance

## Maintenance

- Use `organize_all_files.py` to reorganize files
- Keep documentation updated
- Archive old files in `archive/` directory
"""
    
    with open(BASE_DIR / "docs" / "PROJECT_STRUCTURE.md", 'w') as f:
        f.write(structure_doc)
    
    print("  ✓ Updated README.md")
    print("  ✓ Created PROJECT_STRUCTURE.md")

def create_gitignore():
    """Create/update .gitignore file"""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite3

# Logs
*.log
logs/

# Environment variables
.env
.env.local

# OAuth credentials
client_secret.json
oauth_config.json

# Temporary files
temp/
tmp/
*.tmp

# Archive (organized files)
archive/

# Node modules (if any JS dependencies)
node_modules/

# Coverage reports
htmlcov/
.coverage
.pytest_cache/
"""
    
    with open(BASE_DIR / ".gitignore", 'w') as f:
        f.write(gitignore_content)
    
    print("  ✓ Created/updated .gitignore")

def cleanup_empty_dirs():
    """Remove empty directories after file moves"""
    print("\n🧹 Cleaning up empty directories...")
    
    # Note: Be careful with this - only remove truly empty dirs
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for dir_name in dirs:
            dir_path = Path(root) / dir_name
            try:
                if dir_path.is_dir() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  ✓ Removed empty directory: {dir_path.relative_to(BASE_DIR)}")
            except OSError:
                # Directory not empty or permission error
                pass

def main():
    """Main organization function"""
    print("🎬 MovieHub Project File Organization")
    print("=" * 50)
    
    try:
        # Create directory structure
        create_directories()
        
        # Move files to organized structure
        move_files()
        
        # Create documentation
        create_documentation()
        
        # Create .gitignore
        create_gitignore()
        
        # Clean up empty directories
        cleanup_empty_dirs()
        
        print("\n" + "=" * 50)
        print("✅ File organization completed successfully!")
        print("\n📋 Summary:")
        print("  • Files organized into logical directory structure")
        print("  • Documentation created and updated")
        print("  • README.md updated with project overview")
        print("  • .gitignore created for better version control")
        print("\n🎯 Next Steps:")
        print("  1. Review the organized structure")
        print("  2. Update any hardcoded file paths in scripts")
        print("  3. Test the application to ensure everything works")
        print("  4. Commit the organized structure to version control")
        
    except Exception as e:
        print(f"\n❌ Error during organization: {e}")
        print("Please check the error and try again.")

if __name__ == "__main__":
    main()
