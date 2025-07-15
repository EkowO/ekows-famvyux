import json
import csv
import requests
import time
import pandas as pd
from typing import List, Dict, Set
import os

def load_existing_movies(file_path: str) -> List[Dict]:
    """Load existing movies from the JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def get_existing_movie_titles(movies: List[Dict]) -> Set[str]:
    """Extract all existing movie titles from the current dataset"""
    existing_titles = set()
    for movie in movies:
        title = movie.get('Title', '').lower().strip()
        if title:
            existing_titles.add(title)
    return existing_titles

def read_imdb_csv(csv_file: str) -> List[Dict]:
    """Read movies from the new IMDB CSV file"""
    csv_movies = []
    
    try:
        df = pd.read_csv(csv_file)
        print(f"📊 CSV contains {len(df)} movies")
        
        for _, row in df.iterrows():
            title = str(row.get('Title', '')).strip()
            if title and title != 'nan':
                csv_movies.append({
                    'title': title,
                    'year': str(row.get('Year', '')),
                    'rating': str(row.get('Rating', '')),
                    'genre': str(row.get('Genre', '')),
                    'director': str(row.get('Director', '')),
                    'actors': str(row.get('Actors', '')),
                    'runtime': str(row.get('Runtime (Minutes)', '')),
                    'description': str(row.get('Description', '')),
                    'votes': str(row.get('Votes', '')),
                    'revenue': str(row.get('Revenue (Millions)', '')),
                    'metascore': str(row.get('Metascore', ''))
                })
                
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []
    
    return csv_movies

def fetch_movie_from_omdb(title: str, year: str = None, api_key: str = '984b4107') -> Dict:
    """Fetch movie details from OMDB API"""
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    if year and year != 'nan':
        url += f"&y={year}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            # Try without year if it failed with year
            if year:
                url_no_year = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
                response = requests.get(url_no_year, timeout=10)
                data = response.json()
                if data.get("Response") == "True":
                    return data
            print(f"❌ OMDB API error for '{title}': {data.get('Error', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Request error for '{title}': {e}")
        return None

def convert_csv_to_omdb_format(csv_movie: Dict) -> Dict:
    """Convert CSV format movie to OMDB format using available data"""
    
    # Create basic OMDB structure with CSV data as fallback
    omdb_movie = {
        "Title": csv_movie.get('title', 'N/A'),
        "Year": csv_movie.get('year', 'N/A'),
        "Rated": "N/A",  # Not available in CSV
        "Released": "N/A",  # Not available in CSV
        "Runtime": f"{csv_movie.get('runtime', 'N/A')} min" if csv_movie.get('runtime', 'N/A') != 'N/A' else "N/A",
        "Genre": csv_movie.get('genre', 'N/A'),
        "Director": csv_movie.get('director', 'N/A'),
        "Writer": "N/A",  # Not available in CSV
        "Actors": csv_movie.get('actors', 'N/A'),
        "Plot": csv_movie.get('description', 'N/A'),
        "Language": "English",  # Assumption for IMDB top movies
        "Country": "N/A",  # Not available in CSV
        "Awards": "N/A",  # Not available in CSV
        "Poster": "N/A",  # Not available in CSV
        "Ratings": [
            {
                "Source": "Internet Movie Database",
                "Value": f"{csv_movie.get('rating', 'N/A')}/10"
            }
        ],
        "Metascore": csv_movie.get('metascore', 'N/A'),
        "imdbRating": csv_movie.get('rating', 'N/A'),
        "imdbVotes": csv_movie.get('votes', 'N/A'),
        "imdbID": f"csv_{csv_movie.get('title', '').replace(' ', '_').lower()}",  # Generate fake ID
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": f"${float(csv_movie.get('revenue', 0)) * 1000000:,.0f}" if csv_movie.get('revenue') and csv_movie.get('revenue') != 'nan' else "N/A",
        "Production": "N/A",
        "Website": "N/A",
        "Response": "True"
    }
    
    return omdb_movie

def main():
    # Paths
    csv_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\IMDB-Movie-Data.csv"
    existing_movies_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\all_10000_movies.json"
    
    print("🎬 Loading existing movies...")
    existing_movies = load_existing_movies(existing_movies_file)
    print(f"📊 Found {len(existing_movies)} existing movies")
    
    # Get existing movie titles
    existing_titles = get_existing_movie_titles(existing_movies)
    print(f"📝 Extracted {len(existing_titles)} unique movie titles")
    
    print("\n📁 Reading CSV file...")
    csv_movies = read_imdb_csv(csv_file)
    
    if not csv_movies:
        print("❌ No movies found in CSV file")
        return
    
    # Find movies not in existing database
    new_movies_to_fetch = []
    for csv_movie in csv_movies:
        title_lower = csv_movie['title'].lower().strip()
        if title_lower not in existing_titles:
            new_movies_to_fetch.append(csv_movie)
    
    print(f"🔍 Found {len(new_movies_to_fetch)} new movies to add")
    
    if not new_movies_to_fetch:
        print("✅ All CSV movies are already in the database!")
        return
    
    # Ask user how many to add
    print(f"\nOptions:")
    print(f"1. Add all {len(new_movies_to_fetch)} movies using OMDB API (slower, more complete data)")
    print(f"2. Add all {len(new_movies_to_fetch)} movies using CSV data only (faster, less complete)")
    print(f"3. Add a limited number using OMDB API")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    if choice == "1":
        movies_to_process = new_movies_to_fetch
        use_omdb = True
    elif choice == "2":
        movies_to_process = new_movies_to_fetch
        use_omdb = False
    elif choice == "3":
        try:
            limit = int(input(f"How many movies to add (max {len(new_movies_to_fetch)}): "))
            movies_to_process = new_movies_to_fetch[:limit]
            use_omdb = True
        except ValueError:
            print("❌ Invalid input. Exiting.")
            return
    else:
        print("❌ Invalid choice. Exiting.")
        return
    
    # Create backup
    backup_file = existing_movies_file.replace('.json', '_backup.json')
    print(f"\n💾 Creating backup: {backup_file}")
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(existing_movies, f, ensure_ascii=False, indent=2)
        print("✅ Backup created successfully")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return
    
    # Process movies
    successfully_added = []
    failed_movies = []
    
    print(f"\n🌐 Processing {len(movies_to_process)} movies...")
    
    for i, csv_movie in enumerate(movies_to_process, 1):
        title = csv_movie['title']
        year = csv_movie['year']
        
        print(f"[{i}/{len(movies_to_process)}] Processing: {title} ({year})")
        
        if use_omdb:
            # Try to get complete data from OMDB
            omdb_movie = fetch_movie_from_omdb(title, year)
            if omdb_movie:
                successfully_added.append(omdb_movie)
                print(f"✅ Added from OMDB: {omdb_movie['Title']} ({omdb_movie['Year']}) - Rating: {omdb_movie.get('imdbRating', 'N/A')}")
            else:
                # Fallback to CSV data
                csv_based_movie = convert_csv_to_omdb_format(csv_movie)
                successfully_added.append(csv_based_movie)
                print(f"✅ Added from CSV: {csv_based_movie['Title']} ({csv_based_movie['Year']}) - Rating: {csv_based_movie.get('imdbRating', 'N/A')}")
            
            # Rate limiting for OMDB API
            time.sleep(0.2)
        else:
            # Use only CSV data
            csv_based_movie = convert_csv_to_omdb_format(csv_movie)
            successfully_added.append(csv_based_movie)
            print(f"✅ Added from CSV: {csv_based_movie['Title']} ({csv_based_movie['Year']}) - Rating: {csv_based_movie.get('imdbRating', 'N/A')}")
    
    # Save updated movies
    if successfully_added:
        updated_movies = existing_movies + successfully_added
        
        try:
            with open(existing_movies_file, 'w', encoding='utf-8') as f:
                json.dump(updated_movies, f, ensure_ascii=False, indent=2)
            print(f"\n✅ Successfully updated movie database!")
            print(f"📊 Total movies: {len(updated_movies)} (added {len(successfully_added)})")
            
        except Exception as e:
            print(f"❌ Error saving updated movies: {e}")
            print("🔄 Restoring from backup...")
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                with open(existing_movies_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                print("✅ Restored from backup")
            except Exception as restore_error:
                print(f"❌ Error restoring backup: {restore_error}")
    
    # Final statistics
    print(f"\n📊 Final Statistics:")
    print(f"   🎬 Total movies in database: {len(existing_movies) + len(successfully_added)}")
    print(f"   ➕ New movies added: {len(successfully_added)}")
    print(f"   ❌ Movies failed to fetch: {len(failed_movies)}")
    
    if use_omdb:
        print(f"\n💡 Tip: Movies were fetched from OMDB API for complete data when possible,")
        print(f"   with CSV fallback for movies not found in OMDB.")

if __name__ == "__main__":
    main()
