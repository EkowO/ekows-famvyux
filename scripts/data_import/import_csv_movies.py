import json
import csv
import requests
import time
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

def read_csv_movies(csv_file: str) -> List[Dict]:
    """Read movies from CSV file and extract unique titles"""
    csv_movies = []
    seen_titles = set()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                title = row.get('title', '').strip()
                if title and title.lower() not in seen_titles:
                    seen_titles.add(title.lower())
                    csv_movies.append({
                        'title': title,
                        'director': row.get('director', ''),
                        'release_year': row.get('release_year', ''),
                        'runtime': row.get('runtime', ''),
                        'genre': row.get('genre', ''),
                        'rating': row.get('rating', ''),
                        'metascore': row.get('metascore', ''),
                        'gross': row.get('gross(M)', '')
                    })
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []
    
    return csv_movies

def fetch_movie_from_omdb(title: str, year: str = None, api_key: str = '984b4107') -> Dict:
    """Fetch movie details from OMDB API"""
    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    if year:
        url += f"&y={year}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("Response") == "True":
            return data
        else:
            print(f"❌ OMDB API error for '{title}': {data.get('Error', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"❌ Request error for '{title}': {e}")
        return None

def main():
    # Paths
    csv_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\imdb_clean.csv"
    existing_movies_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\all_10000_movies.json"
    
    print("🎬 Loading existing movies...")
    existing_movies = load_existing_movies(existing_movies_file)
    print(f"📊 Found {len(existing_movies)} existing movies")
    
    # Get existing movie titles
    existing_titles = get_existing_movie_titles(existing_movies)
    print(f"📝 Extracted {len(existing_titles)} unique movie titles")
    
    print("\n📁 Reading CSV file...")
    csv_movies = read_csv_movies(csv_file)
    print(f"📊 Found {len(csv_movies)} unique movies in CSV")
    
    # Find movies not in existing database
    new_movies_to_fetch = []
    for csv_movie in csv_movies:
        title_lower = csv_movie['title'].lower().strip()
        if title_lower not in existing_titles:
            new_movies_to_fetch.append(csv_movie)
    
    print(f"🔍 Found {len(new_movies_to_fetch)} new movies to fetch from OMDB")
    
    if not new_movies_to_fetch:
        print("✅ All CSV movies are already in the database!")
        return
    
    # Ask user how many to add
    print(f"\nDo you want to add all {len(new_movies_to_fetch)} movies?")
    response = input("Enter 'y' for yes, or a number to limit how many to add: ").strip().lower()
    
    if response == 'y' or response == 'yes':
        movies_to_process = new_movies_to_fetch
    else:
        try:
            limit = int(response)
            movies_to_process = new_movies_to_fetch[:limit]
        except ValueError:
            print("❌ Invalid input. Exiting.")
            return
    
    print(f"\n🌐 Fetching {len(movies_to_process)} movies from OMDB API...")
    
    # Create backup
    backup_file = existing_movies_file.replace('.json', '_backup.json')
    print(f"💾 Creating backup: {backup_file}")
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(existing_movies, f, ensure_ascii=False, indent=2)
        print("✅ Backup created successfully")
    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return
    
    # Fetch movies from OMDB
    successfully_added = []
    failed_movies = []
    
    for i, csv_movie in enumerate(movies_to_process, 1):
        title = csv_movie['title']
        year = csv_movie['release_year']
        
        print(f"[{i}/{len(movies_to_process)}] Fetching: {title} ({year})")
        
        omdb_movie = fetch_movie_from_omdb(title, year)
        if omdb_movie:
            successfully_added.append(omdb_movie)
            print(f"✅ Added: {omdb_movie['Title']} ({omdb_movie['Year']}) - Rating: {omdb_movie.get('imdbRating', 'N/A')}")
        else:
            failed_movies.append(f"{title} ({year})")
        
        # Rate limiting
        time.sleep(0.2)
    
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
    
    if failed_movies:
        print(f"\n❌ Failed to fetch {len(failed_movies)} movies:")
        for failed in failed_movies[:10]:  # Show first 10
            print(f"   • {failed}")
        if len(failed_movies) > 10:
            print(f"   ... and {len(failed_movies) - 10} more")

if __name__ == "__main__":
    main()
