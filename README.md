# 🎬 MovieHub - AI-Powered Movie Recommendation System

A sophisticated movie recommendation web application built with FastAPI, featuring AI-powered suggestions, Google OAuth authentication, and a modern IMDB-inspired design.

## 📁 Project Structure

```
ekows-famvyux/
├── 📂 app/                     # Core application code
│   ├── __init__.py
│   ├── config.py               # Application configuration
│   ├── utils.py                # Utility functions
│   ├── routes_movies.py        # Movie browsing routes
│   ├── routes_auth.py          # Authentication routes  
│   ├── routes_ai_suggestions.py # AI recommendation routes
│   ├── routes_comments.py      # Comment system routes
│   ├── routes_watch_later.py   # Watch later functionality
│   └── routes_google_auth.py   # Google OAuth integration
│
├── 📂 static/                  # Web assets
│   └── styles.css              # Main stylesheet with MovieHub theme
│
├── 📂 templates/               # HTML templates
│   ├── base.html               # Base template with navbar
│   ├── browse_movies.html      # Movie browsing with AI chat
│   ├── movie_detail.html       # Individual movie pages
│   ├── liked_movies.html       # User's liked movies
│   └── watch_later.html        # Watch later list
│
├── 📂 scripts/                 # Organized utility scripts
│   ├── 📂 data_import/         # Data import and management
│   │   ├── add_movies.py
│   │   ├── add_popular_movies.py  
│   │   ├── download_imdb_csv.py
│   │   ├── import_csv_movies.py
│   │   ├── import_imdb_top1000.py
│   │   └── update_comments_with_timestamps.py
│   │
│   ├── 📂 testing/             # All test files
│   │   ├── test_ai_manual.py
│   │   ├── test_ai_server.py
│   │   ├── test_ai_styling.py
│   │   ├── test_ai_suggestions.py
│   │   ├── test_and_start_server.py
│   │   ├── test_chatbot_css.py
│   │   ├── test_css.html
│   │   ├── test_css_server.py
│   │   ├── test_environment.bat
│   │   ├── test_google_oauth.py
│   │   ├── test_imports.py
│   │   ├── test_oauth.py
│   │   ├── test_server.py
│   │   ├── minimal_test.py
│   │   ├── minimal_server_test.py
│   │   └── complete_functionality_test.py
│   │
│   ├── 📂 setup/               # Setup and installation scripts
│   │   ├── setup_google_oauth.py
│   │   ├── setup_google_oauth_complete.py
│   │   ├── enable_google_oauth.py
│   │   ├── fix_css_and_start.ps1
│   │   └── fix_css_and_start.bat
│   │
│   ├── 📂 debugging/           # Debugging and diagnostic tools
│   │   ├── debug_ai_bot.py
│   │   ├── debug_ai_error.py
│   │   ├── diagnose_css.py
│   │   ├── complete_ai_diagnosis.py
│   │   ├── comprehensive_diagnosis.py
│   │   ├── simple_ai_diagnosis.py
│   │   └── simple_utils_test.py
│   │
│   └── 📂 utilities/           # Server and utility scripts
│       ├── start_ai_server.py
│       ├── start_debug_server.py
│       ├── start_moviehub_ai.py
│       ├── start_server.py
│       ├── final_server.py
│       └── quick_ai_test.py
│
├── 📂 docs/                    # Documentation
│   ├── AI_MOVIE_FEATURES.md    # AI feature documentation
│   ├── AI_STYLING_UPDATE.md    # Styling guide
│   ├── CSS_TROUBLESHOOTING.md  # CSS debugging guide
│   ├── FIX_SUMMARY.md          # Bug fix summary
│   ├── GOOGLE_OAUTH_SETUP.md   # OAuth setup guide
│   └── GOOGLE_OAUTH_STATUS.md  # OAuth implementation status
│
├── 📂 config/                  # Configuration files
│   └── oauth_config.py         # OAuth credentials configuration
│
├── 📂 data/                    # Data files
│   └── get movies/             # Movie data imports
│
├── 📄 main.py                  # Main application entry point
├── 📄 requirements.txt         # Python dependencies
└── 📄 README.md               # This file
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Application
```bash
python main.py
# or
python -m uvicorn main:app --reload --port 8000
```

### 3. Access the Application
- **Main App**: http://localhost:8000
- **Browse Movies**: http://localhost:8000/browse
- **AI Chat**: Available on browse page

## ✨ Key Features

### 🤖 AI Movie Recommendations
- Intelligent movie suggestions based on user preferences
- Natural language chat interface
- Personalized recommendations with explanations
- Integration with movie database

### 🎨 Modern UI Design
- IMDB-inspired dark theme
- MovieHub branding with signature gold (#f5c518) accents
- Responsive design for all devices
- Smooth animations and hover effects

### 🔐 Authentication System
- Google OAuth integration
- Session management
- User preferences and watch lists

### 🎬 Movie Features
- Browse extensive movie catalog
- Search and filter functionality
- Movie details with ratings and descriptions
- Like/unlike movies
- Watch later lists
- Comment system

## 🛠️ Development Tools

### Testing
Run tests from the `scripts/testing/` directory:
```bash
python scripts/testing/test_ai_suggestions.py
python scripts/testing/test_server.py
```

### Debugging
Use diagnostic tools from `scripts/debugging/`:
```bash
python scripts/debugging/diagnose_css.py
python scripts/debugging/debug_ai_bot.py
```

### Setup Scripts
Initial setup helpers in `scripts/setup/`:
```bash
python scripts/setup/setup_google_oauth.py
# or on Windows:
scripts/setup/fix_css_and_start.bat
```

## 📊 Data Management

Import movie data using scripts in `scripts/data_import/`:
```bash
python scripts/data_import/import_imdb_top1000.py
python scripts/data_import/add_popular_movies.py
```

## 🔧 Configuration

### Google OAuth Setup
1. Configure credentials in `config/oauth_config.py`
2. Follow the guide in `docs/GOOGLE_OAUTH_SETUP.md`

### Environment Variables
Create a `.env` file with:
```
SECRET_KEY=your_secret_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

## 📖 Documentation

Detailed documentation available in the `docs/` folder:
- **AI Features**: `docs/AI_MOVIE_FEATURES.md`
- **CSS Troubleshooting**: `docs/CSS_TROUBLESHOOTING.md`
- **OAuth Setup**: `docs/GOOGLE_OAUTH_SETUP.md`

## 🐛 Troubleshooting

### Common Issues

1. **CSS Not Loading**: See `docs/CSS_TROUBLESHOOTING.md`
2. **AI Chat Not Working**: Run `scripts/debugging/debug_ai_bot.py`
3. **Server Issues**: Use `scripts/debugging/comprehensive_diagnosis.py`

### Quick Fixes
```bash
# Clear cache and restart
rm -rf __pycache__
python main.py

# Test CSS loading
python scripts/testing/test_css_server.py

# Check AI functionality  
python scripts/testing/test_ai_suggestions.py
```

## 🤝 Contributing

1. Keep the organized file structure
2. Add new scripts to appropriate `scripts/` subdirectories
3. Update documentation in `docs/` folder
4. Test changes with scripts in `scripts/testing/`

## 📜 License

This project is licensed under the MIT License.

---

**MovieHub** - Discover your next favorite movie with AI-powered recommendations! 🎬✨
