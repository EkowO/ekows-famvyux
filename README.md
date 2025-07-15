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

2. **Setup Data Files**:
   ```bash
   python scripts/setup/setup_data_files.py
   ```
   
   **Note**: Due to GitHub file size limits, large movie datasets are not included in the repository. The setup script creates sample data for testing. See [Data Setup Instructions](data/DATA_SETUP.md) for full dataset setup.

3. **Run the Application**:
   ```bash
   python main.py
   ```

4. **Access the Application**:
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

## Data Setup

Due to GitHub's file size restrictions, large movie datasets are not included in the repository. You have several options:

### Option 1: Quick Start (Recommended)
```bash
python scripts/setup/setup_data_files.py
```
This creates sample data with 3 movies for immediate testing.

### Option 2: Full Dataset
1. Download TMDB or IMDB datasets
2. Place them in `data/get movies/` directory
3. Run the merge scripts provided
4. See [Data Setup Guide](data/DATA_SETUP.md) for detailed instructions

### Required Data Files
- `all_10000_movies.json` - Main movie database
- `movie_likes.json` - User preferences
- `watch_later.json` - Watchlists
- `users.json` - User accounts
- `comments.json` - Movie comments

## Documentation

- [Data Setup Guide](data/DATA_SETUP.md)
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
