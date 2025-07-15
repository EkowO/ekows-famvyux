import requests
import json
import time
import pandas as pd
from collections import Counter
import re

# API configuration
api_key = '984b4107'

def load_existing_movies():
    """Load existing movies from JSON file"""
    with open('all_10000_movies.json', 'r', encoding='utf-8') as f:
        existing_movies = json.load(f)
    return existing_movies

def get_existing_titles(movies):
    """Get set of existing movie titles"""
    return set(movie['Title'].lower() for movie in movies)

def extract_titles_from_reviews(num_reviews=10000):
    """Extract potential movie titles from reviews"""
    print(f"Analyzing {num_reviews} reviews for movie titles...")
    
    df = pd.read_csv('IMDB Dataset.csv')
    sample_reviews = df['review'].head(num_reviews).tolist()
    
    potential_titles = []
    
    for review in sample_reviews:
        # Look for quoted titles
        quoted_titles = re.findall(r'"([^"]{2,50})"', review)
        single_quoted_titles = re.findall(r"'([^']{2,50})'", review)
        
        # Look for common movie title patterns
        # Movies often mentioned as "Movie Name is..." or "Movie Name was..."
        title_patterns = re.findall(r'\b([A-Z][a-zA-Z\s]{2,30})\s+(?:is|was|will be|has been|had been)\s+(?:a|an|the|one of|about|really|very|quite|so|such|pretty|truly|absolutely)', review)
        
        potential_titles.extend(quoted_titles)
        potential_titles.extend(single_quoted_titles)
        potential_titles.extend(title_patterns)
    
    # Clean and filter titles
    cleaned_titles = []
    for title in potential_titles:
        title = title.strip()
        # Filter out common non-movie phrases
        if (len(title) > 2 and 
            len(title) < 100 and 
            not title.lower() in ['the', 'and', 'or', 'but', 'if', 'then', 'so', 'this', 'that', 'film', 'movie', 'show', 'series'] and
            not title.isdigit() and
            not title.lower().startswith('http')):
            cleaned_titles.append(title)
    
    # Count occurrences and return most common
    title_counts = Counter(cleaned_titles)
    return title_counts

def fetch_popular_movies_by_year(start_year=1990, end_year=2024):
    """Fetch popular movies by year using OMDB API"""
    popular_movies = []
    
    # Common popular movie titles to search for
    popular_titles = [
        # Recent popular movies
        "Top Gun: Maverick", "Spider-Man: No Way Home", "Dune", "The Batman",
        "Avengers: Endgame", "Avatar", "Titanic", "Star Wars", "Jurassic Park",
        "The Lord of the Rings", "Harry Potter", "Iron Man", "The Dark Knight",
        "Inception", "Interstellar", "Gladiator", "The Matrix", "Pulp Fiction",
        "Forrest Gump", "The Lion King", "Toy Story", "Finding Nemo", "Shrek",
        "Pirates of the Caribbean", "Indiana Jones", "Back to the Future",
        "E.T.", "Jaws", "Rocky", "Terminator", "Alien", "Blade Runner",
        "Casablanca", "Gone with the Wind", "The Wizard of Oz", "Citizen Kane",
        
        # Action movies
        "Mad Max: Fury Road", "John Wick", "Mission: Impossible", "Fast & Furious",
        "Die Hard", "Lethal Weapon", "The Bourne Identity", "Casino Royale",
        "Skyfall", "Wonder Woman", "Black Panther", "Captain America", "Thor",
        
        # Comedy movies
        "The Hangover", "Anchorman", "Superbad", "Knocked Up", "Wedding Crashers",
        "Meet the Parents", "There's Something About Mary", "Dumb and Dumber",
        "The Big Lebowski", "Zoolander", "Dodgeball", "Old School",
        
        # Drama movies
        "The Social Network", "The Departed", "No Country for Old Men",
        "There Will Be Blood", "Moonlight", "La La Land", "The Revenant",
        "Birdman", "12 Years a Slave", "The King's Speech", "Slumdog Millionaire",
        
        # Horror movies
        "Get Out", "A Quiet Place", "Hereditary", "The Conjuring", "Insidious",
        "Paranormal Activity", "Saw", "The Ring", "The Grudge", "Scream",
        
        # Sci-Fi movies
        "Blade Runner 2049", "Arrival", "Ex Machina", "Gravity", "Pacific Rim",
        "District 9", "Elysium", "Oblivion", "Edge of Tomorrow", "Looper",
        
        # Fantasy movies
        "The Chronicles of Narnia", "The Golden Compass", "Pan's Labyrinth",
        "The Shape of Water", "Big Fish", "Edward Scissorhands", "The NeverEnding Story",
        
        # Animated movies
        "Frozen", "Moana", "Coco", "Inside Out", "Up", "WALL-E", "Ratatouille",
        "The Incredibles", "Monsters, Inc.", "Finding Dory", "Zootopia", "Big Hero 6"
    ]
    
    return popular_titles

def search_and_add_movies(existing_movies, existing_titles, search_list):
    """Search for movies using OMDB API and add new ones"""
    new_movies = []
    
    for i, title in enumerate(search_list):
        print(f"Searching {i+1}/{len(search_list)}: {title}")
        
        try:
            # Search for the movie
            resp = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={api_key}")
            data = resp.json()
            
            if data.get("Response") == "True":
                # Check if we already have this movie
                if data['Title'].lower() not in existing_titles:
                    new_movies.append(data)
                    existing_titles.add(data['Title'].lower())
                    print(f"  ✓ Added: {data['Title']} ({data['Year']})")
                else:
                    print(f"  - Already exists: {data['Title']}")
            else:
                print(f"  ✗ Not found: {data.get('Error', 'Unknown error')}")
                
        except Exception as e:
            print(f"  ✗ Error searching {title}: {e}")
        
        # Rate limiting
        time.sleep(0.1)
    
    return new_movies

def main():
    print("Loading existing movies...")
    existing_movies = load_existing_movies()
    existing_titles = get_existing_titles(existing_movies)
    
    print(f"Current movies in JSON: {len(existing_movies)}")
    print(f"Unique titles: {len(existing_titles)}")
    
    # Method 1: Extract titles from reviews
    print("\n" + "="*50)
    print("METHOD 1: Extracting titles from reviews")
    print("="*50)
    
    review_titles = extract_titles_from_reviews(5000)
    top_review_titles = [title for title, count in review_titles.most_common(100) if count >= 2]
    
    print(f"Found {len(top_review_titles)} potential movie titles from reviews")
    
    if top_review_titles:
        print("Adding movies from reviews...")
        new_movies_from_reviews = search_and_add_movies(existing_movies, existing_titles, top_review_titles)
        existing_movies.extend(new_movies_from_reviews)
        print(f"Added {len(new_movies_from_reviews)} movies from reviews")
    
    # Method 2: Popular movies
    print("\n" + "="*50)
    print("METHOD 2: Adding popular movies")
    print("="*50)
    
    popular_titles = fetch_popular_movies_by_year()
    print(f"Searching for {len(popular_titles)} popular movies...")
    
    new_movies_popular = search_and_add_movies(existing_movies, existing_titles, popular_titles)
    existing_movies.extend(new_movies_popular)
    print(f"Added {len(new_movies_popular)} popular movies")
    
    # Save updated JSON
    print("\n" + "="*50)
    print("SAVING RESULTS")
    print("="*50)
    
    with open('all_10000_movies.json', 'w', encoding='utf-8') as f:
        json.dump(existing_movies, f, indent=4)
    
    total_added = len(new_movies_from_reviews) + len(new_movies_popular)
    print(f"Total new movies added: {total_added}")
    print(f"Total movies in JSON now: {len(existing_movies)}")
    
    # Show some statistics
    years = [int(movie['Year']) for movie in existing_movies if movie['Year'].isdigit()]
    if years:
        print(f"Year range: {min(years)} - {max(years)}")
        
    genres = []
    for movie in existing_movies:
        if movie.get('Genre'):
            genres.extend([g.strip() for g in movie['Genre'].split(',')])
    
    if genres:
        genre_counts = Counter(genres)
        print("Top 10 genres:")
        for genre, count in genre_counts.most_common(10):
            print(f"  {genre}: {count} movies")

if __name__ == "__main__":
    main()
