import json
import hashlib
import os
from .config import MOVIES_FILE, LIKES_FILE, WATCH_LATER_FILE, USERS_FILE, COMMENTS_FILE

# TMDB base URL for poster images
TMDB_POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

def fix_poster_url(poster_url):
    """Fix poster URLs to ensure they are complete and valid"""
    if not poster_url or poster_url == 'N/A':
        return '/static/no-poster.png'
    
    # If it's already a full URL (like Amazon posters), return as-is
    if poster_url.startswith('http'):
        return poster_url
    
    # If it's a TMDB relative path (starts with /), prepend the base URL
    if poster_url.startswith('/'):
        return f"{TMDB_POSTER_BASE_URL}{poster_url}"
    
    # For any other case, return a fallback
    return '/static/no-poster.png'

def process_movie_posters(movies):
    """Process a list of movies to fix their poster URLs"""
    if isinstance(movies, dict):
        # Single movie
        if 'Poster' in movies:
            movies['Poster'] = fix_poster_url(movies['Poster'])
        return movies
    elif isinstance(movies, list):
        # List of movies
        for movie in movies:
            if 'Poster' in movie:
                movie['Poster'] = fix_poster_url(movie['Poster'])
        return movies
    return movies

def load_movies():
    with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
        movies = json.load(f)
    # Fix poster URLs when loading
    return process_movie_posters(movies)

def save_movies(movies):
    with open(MOVIES_FILE, 'w', encoding='utf-8') as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

def load_likes():
    if not os.path.exists(LIKES_FILE):
        return {}
    with open(LIKES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_likes(likes):
    with open(LIKES_FILE, 'w', encoding='utf-8') as f:
        json.dump(likes, f)

def load_watch_later():
    if not os.path.exists(WATCH_LATER_FILE):
        return {}
    with open(WATCH_LATER_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_watch_later(watch_later):
    with open(WATCH_LATER_FILE, 'w', encoding='utf-8') as f:
        json.dump(watch_later, f)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f)

def load_comments():
    if not os.path.exists(COMMENTS_FILE):
        return {}
    with open(COMMENTS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_comments(comments):
    with open(COMMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(comments, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_all_unique_movies(movies):
    unique_movies = {}
    for movie in movies:
        imdb_id = movie.get('imdbID')
        if imdb_id and imdb_id not in unique_movies:
            unique_movies[imdb_id] = movie
    return list(unique_movies.values())

def get_child_unique_movies(movies):
    unique_movies = {}
    for movie in movies:
        imdb_id = movie.get('imdbID')
        if imdb_id and imdb_id not in unique_movies and movie.get('Rated') in ['G', 'PG', 'PG-13']:
            unique_movies[imdb_id] = movie
    return list(unique_movies.values())

def get_final_top_movies_by_genre(movies):
    genre_movies = {}
    
    for movie in movies:
        genres = movie.get('Genre', '').split(', ')
        
        for genre in genres:
            if genre and genre != 'N/A':
                if genre not in genre_movies:
                    genre_movies[genre] = []
                
                if len(genre_movies[genre]) < 10:
                    genre_movies[genre].append(movie)
    
    return genre_movies

def organize_movies_by_genre(movies):
    """Organize a list of movies by genre, limiting to 10 per genre"""
    genre_movies = {}
    
    for movie in movies:
        genres = movie.get('Genre', '').split(', ')
        
        for genre in genres:
            if genre and genre != 'N/A':
                if genre not in genre_movies:
                    genre_movies[genre] = []
                
                # Add movie to genre if not already present and under limit
                if movie not in genre_movies[genre] and len(genre_movies[genre]) < 10:
                    genre_movies[genre].append(movie)
    
    return genre_movies

def search_movies(movies, query):
    """Search movies by title, actors, director, or genre"""
    if not query:
        return movies
    
    query = query.lower()
    results = []
    
    for movie in movies:
        # Search in title
        if query in movie.get('Title', '').lower():
            results.append(movie)
            continue
        
        # Search in actors
        if query in movie.get('Actors', '').lower():
            results.append(movie)
            continue
        
        # Search in director
        if query in movie.get('Director', '').lower():
            results.append(movie)
            continue
        
        # Search in genre
        if query in movie.get('Genre', '').lower():
            results.append(movie)
            continue
    
    return results

def filter_movies(movies, query="", genre="", min_rating=None, max_rating=None, year_from=None, year_to=None, rated=""):
    """Filter movies based on various criteria"""
    filtered = movies
    
    # Search by query first
    if query:
        filtered = search_movies(filtered, query)
    
    # Filter by genre
    if genre:
        filtered = [m for m in filtered if genre.lower() in m.get('Genre', '').lower()]
    
    # Filter by rating
    if min_rating is not None or max_rating is not None:
        filtered_by_rating = []
        for movie in filtered:
            try:
                rating = float(movie.get('imdbRating', 0))
                if min_rating is not None and rating < min_rating:
                    continue
                if max_rating is not None and rating > max_rating:
                    continue
                filtered_by_rating.append(movie)
            except (ValueError, TypeError):
                # Skip movies with invalid ratings
                pass
        filtered = filtered_by_rating
    
    # Filter by year
    if year_from is not None or year_to is not None:
        filtered_by_year = []
        for movie in filtered:
            try:
                year = int(movie.get('Year', 0))
                if year_from is not None and year < year_from:
                    continue
                if year_to is not None and year > year_to:
                    continue
                filtered_by_year.append(movie)
            except (ValueError, TypeError):
                # Skip movies with invalid years
                pass
        filtered = filtered_by_year
    
    # Filter by content rating
    if rated:
        filtered = [m for m in filtered if m.get('Rated') == rated]
    
    return filtered

def get_filter_options(movies):
    """Get all available filter options from the movie database"""
    genres = set()
    ratings = set()
    years = set()
    
    for movie in movies:
        # Collect genres
        movie_genres = movie.get('Genre', '').split(', ')
        for genre in movie_genres:
            if genre and genre != 'N/A':
                genres.add(genre)
        
        # Collect content ratings
        rated = movie.get('Rated')
        if rated and rated != 'N/A':
            ratings.add(rated)
        
        # Collect years
        try:
            year = int(movie.get('Year', 0))
            if year > 0:
                years.add(year)
        except (ValueError, TypeError):
            pass
    
    return {
        'genres': sorted(list(genres)),
        'ratings': sorted(list(ratings)),
        'years': sorted(list(years), reverse=True)
    }
