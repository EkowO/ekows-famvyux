# MovieHub - IMDB-Style Movie Database

A modern, responsive movie database application with AI-powered recommendations and comprehensive movie management features.

## Features

- **Movie Database**: Browse, search, and discover movies
- **AI Recommendations**: Intelligent movie suggestions based on preferences
- **User Management**: User accounts with Google OAuth integration
- **Responsive Design**: IMDB-inspired dark theme with mobile support
- **Advanced Filtering**: Multi-column responsive filter system
- **Comments System**: User reviews and ratings
- **Watch Later**: Personal movie watchlist management

## Quick Start

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

## Project Structure

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
│   ├── debugging/          # Debug utilities
│   └── utilities/          # Helper scripts
├── docs/                   # Documentation
├── data/                   # Data files and databases
├── config/                 # Configuration files
└── tests/                  # Test files
```

## Configuration

- **Database**: SQLite database for movie storage
- **Authentication**: Google OAuth integration
- **AI Features**: OpenAI integration for recommendations

## Documentation

- [Setup Guide](docs/setup/)
- [Feature Documentation](docs/features/)
- [Troubleshooting](docs/troubleshooting/)

## Development

- **Framework**: FastAPI
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLite
- **Authentication**: Google OAuth
- **AI**: OpenAI GPT integration

## License

This project is licensed under the MIT License.
