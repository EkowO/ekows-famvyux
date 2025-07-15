import requests
import json
import time
import csv
import pandas as pd

# API key for OMDB
api_key = '984b4107'

# Load existing movies from JSON
with open('all_10000_movies.json', 'r', encoding='utf-8') as f:
    existing_movies = json.load(f)

# Create a set of existing movie titles (convert to lowercase for comparison)
existing_titles = set()
for movie in existing_movies:
    existing_titles.add(movie['Title'].lower())

print(f"Found {len(existing_movies)} movies in JSON file")
print(f"Found {len(existing_titles)} unique titles in JSON file")

# Load CSV data
df = pd.read_csv('imdb_clean.csv')
csv_titles = df['title'].unique()

print(f"Found {len(csv_titles)} unique titles in CSV file")

# Find missing movies
missing_movies = []
for title in csv_titles:
    if title.lower() not in existing_titles:
        missing_movies.append(title)

print(f"Found {len(missing_movies)} movies missing from JSON")

if missing_movies:
    print("Missing movies:")
    for movie in missing_movies:
        print(f"  - {movie}")
    
    # Fetch missing movies from OMDB API
    new_movies = []
    for i, title in enumerate(missing_movies):
        print(f"Fetching {i+1}/{len(missing_movies)}: {title}")
        try:
            resp = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={api_key}")
            data = resp.json()
            if data.get("Response") == "True":
                new_movies.append(data)
                print(f"  ✓ Added: {data['Title']}")
            else:
                print(f"  ✗ Failed: {data.get('Error', 'Unknown error')}")
        except Exception as e:
            print(f"  ✗ Error fetching {title}: {e}")
        
        # Rate limiting
        time.sleep(0.2)
    
    # Add new movies to existing ones
    all_movies = existing_movies + new_movies
    
    # Save updated JSON
    with open('all_10000_movies.json', 'w', encoding='utf-8') as f:
        json.dump(all_movies, f, indent=4)
    
    print(f"\nAdded {len(new_movies)} new movies to JSON file")
    print(f"Total movies in JSON now: {len(all_movies)}")
else:
    print("No missing movies found. All CSV titles are already in the JSON file.")
