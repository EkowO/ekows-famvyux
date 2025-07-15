# Data Setup Instructions

## Important Note about Large Files

Due to GitHub's file size restrictions, the large movie datasets are not included in this repository. You'll need to set up the data files locally to run the application.

## Required Data Files

The following files need to be present in `data/get movies/` directory:

### Essential Files (for basic functionality):
- `all_10000_movies.json` - Main movie database
- `movie_likes.json` - User movie likes
- `watch_later.json` - User watch later lists
- `users.json` - User accounts
- `comments.json` - Movie comments

### Optional Files (for enhanced functionality):
- `TMDB_movie_dataset_v11.csv` - TMDB movie dataset
- `IMDB Dataset.csv` - IMDB movie dataset

## Setup Options

### Option 1: Start with Sample Data (Recommended for Testing)
```bash
# Copy sample data to main movie file
cp "data/get movies/movies_sample.json" "data/get movies/all_10000_movies.json"

# Run the setup script to create other required files
python scripts/setup/setup_data_files.py
```

### Option 2: Download Full Datasets (For Production)

1. **Download TMDB Dataset**:
   - Visit: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
   - Download and place in `data/get movies/` as `TMDB_movie_dataset_v11.csv`

2. **Download IMDB Dataset**:
   - Visit: https://www.imdb.com/interfaces/
   - Download and place in `data/get movies/` as `IMDB Dataset.csv`

3. **Run the merge script**:
   ```bash
   cd "data/get movies"
   python merge_tmdb_movies.py
   ```

### Option 3: Use Existing Data (If Available)
If you have existing movie data files:
1. Place them in `data/get movies/` directory
2. Ensure they follow the JSON format shown in `movies_sample.json`
3. Run the application

## File Formats

### Movie JSON Format
```json
{
  "Title": "Movie Title",
  "Year": "2023",
  "Rated": "PG-13",
  "Runtime": "120 min",
  "Genre": "Action, Drama",
  "Director": "Director Name",
  "Plot": "Movie plot summary",
  "imdbRating": "8.5",
  "imdbID": "tt1234567",
  // ... other fields
}
```

### Other Files
- `movie_likes.json`: `{}`
- `watch_later.json`: `{}`
- `users.json`: `{}`
- `comments.json`: `{}`

## Quick Start Script

Run this command to set up minimal data files:

```bash
python scripts/setup/setup_data_files.py
```

This will create empty JSON files with the correct structure for the application to work.
