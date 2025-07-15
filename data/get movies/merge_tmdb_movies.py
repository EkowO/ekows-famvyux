#!/usr/bin/env python3
"""
TMDB Movie Dataset Merger
Adds unique movies from TMDB dataset to all_10000_movies.json
Converts TMDB format to match existing movie format
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
import re
from pathlib import Path

def clean_text(text):
    """Clean and format text fields"""
    if pd.isna(text) or text == "" or text == "N/A":
        return "N/A"
    return str(text).strip()

def format_runtime(runtime):
    """Convert runtime from minutes to 'X min' format"""
    if pd.isna(runtime) or runtime == 0:
        return "N/A"
    return f"{int(runtime)} min"

def format_year(release_date):
    """Extract year from release date"""
    if pd.isna(release_date) or release_date == "":
        return "N/A"
    try:
        # Parse date and extract year
        if isinstance(release_date, str):
            year = datetime.strptime(release_date, "%Y-%m-%d").year
            return str(year)
    except:
        # Try to extract year from string
        year_match = re.search(r'\b(19|20)\d{2}\b', str(release_date))
        if year_match:
            return year_match.group()
    return "N/A"

def format_rating(vote_average):
    """Convert vote average to IMDB-style rating"""
    if pd.isna(vote_average) or vote_average == 0:
        return "N/A"
    return f"{float(vote_average):.1f}"

def format_genres(genres):
    """Format genres from TMDB format"""
    if pd.isna(genres) or genres == "":
        return "N/A"
    
    # Handle JSON-like genre format
    try:
        if isinstance(genres, str) and genres.startswith('['):
            # Parse JSON-like genre data
            genres_clean = genres.replace("'", '"')
            genre_data = json.loads(genres_clean)
            if isinstance(genre_data, list) and len(genre_data) > 0:
                genre_names = [g.get('name', '') for g in genre_data if isinstance(g, dict)]
                return ", ".join(genre_names[:3])  # Limit to 3 genres
        else:
            # Simple comma-separated format
            genre_list = str(genres).split(',')
            return ", ".join([g.strip() for g in genre_list[:3]])
    except:
        # Fallback: use as is
        return clean_text(genres)
    
    return "N/A"

def convert_tmdb_to_movie_format(tmdb_row):
    """Convert TMDB row to movie format matching all_10000_movies.json"""
    return {
        "Title": clean_text(tmdb_row.get('title', tmdb_row.get('original_title', 'N/A'))),
        "Year": format_year(tmdb_row.get('release_date')),
        "Rated": "N/A",  # TMDB doesn't have MPAA ratings
        "Released": clean_text(tmdb_row.get('release_date')),
        "Runtime": format_runtime(tmdb_row.get('runtime')),
        "Genre": format_genres(tmdb_row.get('genres')),
        "Director": "N/A",  # TMDB dataset doesn't include director
        "Writer": "N/A",   # TMDB dataset doesn't include writer
        "Actors": "N/A",   # TMDB dataset doesn't include actors
        "Plot": clean_text(tmdb_row.get('overview')),
        "Language": clean_text(tmdb_row.get('original_language')),
        "Country": "N/A",  # Would need production_countries parsing
        "Awards": "N/A",
        "Poster": clean_text(tmdb_row.get('poster_path')),
        "Ratings": [
            {
                "Source": "TMDB",
                "Value": format_rating(tmdb_row.get('vote_average'))
            }
        ],
        "Metascore": "N/A",
        "imdbRating": format_rating(tmdb_row.get('vote_average')),
        "imdbVotes": clean_text(tmdb_row.get('vote_count')),
        "imdbID": clean_text(tmdb_row.get('imdb_id')),
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": clean_text(tmdb_row.get('revenue')) if tmdb_row.get('revenue', 0) > 0 else "N/A",
        "Production": "N/A",
        "Website": clean_text(tmdb_row.get('homepage')),
        "Response": "True"
    }

def normalize_title_for_comparison(title):
    """Normalize title for duplicate detection"""
    if not title or title == "N/A":
        return ""
    
    # Convert to lowercase and remove special characters
    normalized = re.sub(r'[^\w\s]', '', title.lower())
    # Remove extra whitespace
    normalized = ' '.join(normalized.split())
    return normalized

def load_existing_movies():
    """Load existing movies from all_10000_movies.json"""
    try:
        with open('all_10000_movies.json', 'r', encoding='utf-8') as f:
            movies = json.load(f)
        print(f"✅ Loaded {len(movies)} existing movies")
        return movies
    except Exception as e:
        print(f"❌ Error loading existing movies: {e}")
        return []

def load_tmdb_dataset():
    """Load TMDB dataset"""
    try:
        print("📁 Loading TMDB dataset...")
        df = pd.read_csv('TMDB_movie_dataset_v11.csv')
        print(f"✅ Loaded {len(df)} movies from TMDB dataset")
        return df
    except Exception as e:
        print(f"❌ Error loading TMDB dataset: {e}")
        return None

def create_duplicate_index(existing_movies):
    """Create index of existing movies for duplicate detection"""
    duplicate_index = set()
    
    for movie in existing_movies:
        title = movie.get('Title', '')
        year = movie.get('Year', '')
        imdb_id = movie.get('imdbID', '')
        
        # Add normalized title-year combination
        normalized_title = normalize_title_for_comparison(title)
        if normalized_title and year != "N/A":
            duplicate_index.add(f"{normalized_title}|{year}")
        
        # Add IMDB ID if available
        if imdb_id and imdb_id != "N/A":
            duplicate_index.add(f"imdb|{imdb_id}")
    
    return duplicate_index

def is_duplicate(movie, duplicate_index):
    """Check if movie is a duplicate"""
    title = movie.get('Title', '')
    year = movie.get('Year', '')
    imdb_id = movie.get('imdbID', '')
    
    # Check normalized title-year combination
    normalized_title = normalize_title_for_comparison(title)
    if normalized_title and year != "N/A":
        title_year_key = f"{normalized_title}|{year}"
        if title_year_key in duplicate_index:
            return True
    
    # Check IMDB ID
    if imdb_id and imdb_id != "N/A":
        imdb_key = f"imdb|{imdb_id}"
        if imdb_key in duplicate_index:
            return True
    
    return False

def filter_quality_movies(df):
    """Filter TMDB movies for quality (optional)"""
    print("🔍 Filtering for quality movies...")
    
    # Filter criteria
    filtered_df = df[
        (df['vote_count'] >= 10) &  # At least 10 votes
        (df['vote_average'] >= 4.0) &  # Minimum rating
        (df['status'] == 'Released') &  # Only released movies
        (~df['adult']) &  # No adult content
        (df['runtime'] >= 60)  # At least 60 minutes (feature films)
    ].copy()
    
    print(f"✅ Filtered to {len(filtered_df)} quality movies")
    return filtered_df

def merge_datasets():
    """Main function to merge TMDB dataset with existing movies"""
    print("🎬 TMDB Movie Dataset Merger")
    print("=" * 50)
    
    # Load existing movies
    existing_movies = load_existing_movies()
    if not existing_movies:
        print("❌ No existing movies found")
        return
    
    # Load TMDB dataset
    tmdb_df = load_tmdb_dataset()
    if tmdb_df is None:
        return
    
    # Filter for quality movies (optional - comment out if you want all movies)
    tmdb_df = filter_quality_movies(tmdb_df)
    
    # Create duplicate detection index
    print("🔍 Creating duplicate detection index...")
    duplicate_index = create_duplicate_index(existing_movies)
    print(f"✅ Created index with {len(duplicate_index)} entries")
    
    # Process TMDB movies and find unique ones
    print("🔄 Processing TMDB movies...")
    new_movies = []
    duplicates_found = 0
    errors = 0
    
    for index, row in tmdb_df.iterrows():
        try:
            # Convert TMDB format to movie format
            movie = convert_tmdb_to_movie_format(row)
            
            # Check for duplicates
            if not is_duplicate(movie, duplicate_index):
                new_movies.append(movie)
                
                # Add to duplicate index to avoid duplicates within TMDB dataset
                title = movie.get('Title', '')
                year = movie.get('Year', '')
                imdb_id = movie.get('imdbID', '')
                
                normalized_title = normalize_title_for_comparison(title)
                if normalized_title and year != "N/A":
                    duplicate_index.add(f"{normalized_title}|{year}")
                if imdb_id and imdb_id != "N/A":
                    duplicate_index.add(f"imdb|{imdb_id}")
            else:
                duplicates_found += 1
                
        except Exception as e:
            errors += 1
            if errors < 10:  # Show first 10 errors
                print(f"⚠️  Error processing row {index}: {e}")
        
        # Progress update
        if (index + 1) % 10000 == 0:
            print(f"   Processed {index + 1}/{len(tmdb_df)} movies... "
                  f"({len(new_movies)} unique, {duplicates_found} duplicates)")
    
    print(f"\n📊 Processing Summary:")
    print(f"   Total TMDB movies processed: {len(tmdb_df)}")
    print(f"   Unique movies found: {len(new_movies)}")
    print(f"   Duplicates skipped: {duplicates_found}")
    print(f"   Errors encountered: {errors}")
    
    if not new_movies:
        print("ℹ️  No new unique movies found to add")
        return
    
    # Create backup of existing file
    print("💾 Creating backup...")
    try:
        with open('all_10000_movies_backup.json', 'w', encoding='utf-8') as f:
            json.dump(existing_movies, f, indent=2)
        print("✅ Backup created: all_10000_movies_backup.json")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return
    
    # Merge with existing movies
    print("🔗 Merging datasets...")
    merged_movies = existing_movies + new_movies
    
    # Save merged dataset
    try:
        with open('all_10000_movies.json', 'w', encoding='utf-8') as f:
            json.dump(merged_movies, f, indent=2)
        
        print(f"✅ Successfully merged datasets!")
        print(f"   Original movies: {len(existing_movies)}")
        print(f"   New movies added: {len(new_movies)}")
        print(f"   Total movies: {len(merged_movies)}")
        
    except Exception as e:
        print(f"❌ Error saving merged dataset: {e}")

def main():
    """Main execution function"""
    try:
        merge_datasets()
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
