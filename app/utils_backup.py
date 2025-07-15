import json
import hashlib
import os
from .config import MOVIES_FILE, LIKES_FILE, WATCH_LATER_FILE, USERS_FILE, COMMENTS_FILE

# TMDB base URL for poster images
TMDB_POSTER_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Base64 encoded placeholder image (140x210 dark gray with "No Image Available" text)
NO_POSTER_PLACEHOLDER = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIwAAADSCAYAAACMdYQ4AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAdgAAAHYBTnsmCAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANYSURBVHic7d1NaxNBGMfx/2ySJm1sW6uttVq1KIqIB/HgwYMXD+LBk6AHQTx48uTVq1c/gAcPXrx49OBBEBQFwYMHL4IH8aAIvtSq1Wpr39o0aZNkH2cns5mdZGeT7OwM/H8wkGQzs8/zm5mdnZ0dAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACA/3FDdwA5qFQqw8aYCWPMhDFm3BgzJiJlESkZY4rGmKIxZlBE+kWkV0R6RKQgIrGIRMaYSESiKIo6nU6n2Ww2W61Wq9FoNOr1er3RaNTr9Xq9Wq1Wa7VarVqtVqvVajXbtm3bWJZlWZZl5f8fLwCnJ8dV3mKxOCQik8aYSWPMFGPMCcaYE40xJxtjTjHGTDHGTLdarcnJycnJycnJqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqanZ7XYLOTwXAH8wxkxzzk/jnJ/JOT+bc36u53luYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCm5iY8CYmJryJiQlvYmLCOzExMTHhTUxMTEhIeIhwzidwzs/knJ/DOT/fc76xsbGxsbGxsbGxsbGxsbGxsb

def fix_poster_url(poster_url):
    """Fix poster URLs to ensure they are complete and valid"""
    if not poster_url or poster_url == 'N/A':
        return NO_POSTER_PLACEHOLDER
    
    # If it's already a full URL (like Amazon posters), return as-is
    if poster_url.startswith('http'):
        return poster_url
    
    # If it's a TMDB relative path (starts with /), prepend the base URL
    if poster_url.startswith('/'):
        return f"{TMDB_POSTER_BASE_URL}{poster_url}"
    
    # For any other case, return a fallback
    return NO_POSTER_PLACEHOLDER

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
    all_unique = {}
    for m in movies:
        title = m.get("Title")
        if (
            title
            and m.get("imdbRating")
            and m.get("Poster")
            and m.get("imdbRating") != "N/A"
            and title not in all_unique
        ):
            all_unique[title] = m
    return all_unique

def get_all_unique_movies_list(movies):
    """Get unique movies as a list for AI processing"""
    all_unique = {}
    for m in movies:
        title = m.get("Title")
        if (
            title
            and m.get("imdbRating")
            and m.get("Poster")
            and m.get("imdbRating") != "N/A"
            and title not in all_unique
        ):
            all_unique[title] = m
    return list(all_unique.values())

def get_child_unique_movies(movies, child_ratings={"G", "PG", "PG-13"}):
    child_unique = {}
    for m in movies:
        title = m.get("Title")
        rated = m.get("Rated")
        if (
            title
            and m.get("imdbRating")
            and m.get("Poster")
            and m.get("imdbRating") != "N/A"
            and rated in child_ratings
            and title not in child_unique
        ):
            child_unique[title] = m
    return child_unique

from collections import defaultdict

def get_final_top_movies_by_genre(child_unique_movies):
    genre_movies = defaultdict(list)
    used_titles = set()
    for movie in child_unique_movies.values():
        genres = [g.strip() for g in movie.get("Genre", "").split(",") if g.strip()]
        if genres:
            first_genre = genres[0]
            if movie["Title"] not in used_titles:
                genre_movies[first_genre].append(movie)
                used_titles.add(movie["Title"])
    final_top = {}
    for genre, movies_list in genre_movies.items():
        valid_movies = []
        for x in movies_list:
            try:
                rating = float(x["imdbRating"])
                valid_movies.append((rating, x))
            except (ValueError, KeyError, TypeError):
                continue
        sorted_movies = [x for _, x in sorted(valid_movies, key=lambda t: t[0], reverse=True)]
        if len(sorted_movies) >= 5:
            final_top[genre] = sorted_movies[:5]
    return final_top

def search_movies(query, all_unique_movies):
    query = query.lower().strip()
    found_movies = []
    for m in all_unique_movies.values():
        if query in m.get("Title", "").lower():
            found_movies.append(m)
    return found_movies

def format_timestamp(timestamp_str):
    """Format timestamp to be more user-friendly"""
    from datetime import datetime
    try:
        dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        diff = now - dt
        
        if diff.days > 0:
            if diff.days == 1:
                return "1 day ago"
            elif diff.days < 7:
                return f"{diff.days} days ago"
            elif diff.days < 30:
                weeks = diff.days // 7
                return f"{weeks} week{'s' if weeks > 1 else ''} ago"
            else:
                months = diff.days // 30
                return f"{months} month{'s' if months > 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
        else:
            return "Just now"
    except:
        return timestamp_str

def get_filter_options(movies_dict):
    """Extract all available filter options from movies"""
    genres = set()
    years = set()
    rated_options = set()
    min_imdb_rating = 10.0
    max_imdb_rating = 0.0
    
    for movie in movies_dict.values():
        # Extract genres
        if movie.get("Genre"):
            movie_genres = [g.strip() for g in movie.get("Genre", "").split(",")]
            genres.update(movie_genres)
        
        # Extract years
        if movie.get("Year"):
            try:
                year = int(movie.get("Year"))
                years.add(year)
            except (ValueError, TypeError):
                pass
        
        # Extract content ratings
        if movie.get("Rated"):
            rated_options.add(movie.get("Rated"))
        
        # Extract IMDB rating range
        if movie.get("imdbRating") and movie.get("imdbRating") != "N/A":
            try:
                rating = float(movie.get("imdbRating"))
                min_imdb_rating = min(min_imdb_rating, rating)
                max_imdb_rating = max(max_imdb_rating, rating)
            except (ValueError, TypeError):
                pass
    
    return {
        "genres": sorted(list(genres)),
        "years": sorted(list(years)),
        "rated_options": sorted(list(rated_options)),
        "min_imdb_rating": min_imdb_rating if min_imdb_rating != 10.0 else 0.0,
        "max_imdb_rating": max_imdb_rating
    }

def filter_movies(movies_dict, query="", genre="", min_rating=None, max_rating=None, 
                 year_from=None, year_to=None, rated=""):
    """Filter movies based on various criteria"""
    filtered_movies = []
    
    for movie in movies_dict.values():
        # Text search filter
        if query and query.lower() not in movie.get("Title", "").lower():
            continue
        
        # Genre filter
        if genre and genre not in movie.get("Genre", ""):
            continue
        
        # IMDB rating filter
        if min_rating is not None or max_rating is not None:
            try:
                movie_rating_str = movie.get("imdbRating", "0")
                if movie_rating_str == "N/A":
                    continue
                movie_rating = float(movie_rating_str)
                if min_rating is not None and movie_rating < min_rating:
                    continue
                if max_rating is not None and movie_rating > max_rating:
                    continue
            except (ValueError, TypeError):
                continue
        
        # Year filter
        if year_from is not None or year_to is not None:
            try:
                movie_year_str = movie.get("Year", "0")
                # Handle year ranges like "2020-2021" by taking the first year
                if "-" in movie_year_str:
                    movie_year_str = movie_year_str.split("-")[0]
                movie_year = int(movie_year_str)
                if year_from is not None and movie_year < year_from:
                    continue
                if year_to is not None and movie_year > year_to:
                    continue
            except (ValueError, TypeError):
                continue
        
        # Content rating filter
        if rated and movie.get("Rated") != rated:
            continue
        
        filtered_movies.append(movie)
    
    return filtered_movies

def organize_movies_by_genre(movies_list, max_per_genre=5):
    """Organize a list of movies by their primary genre"""
    from collections import defaultdict
    
    genre_movies = defaultdict(list)
    used_titles = set()
    
    # Sort movies by rating first (highest first)
    sorted_movies = []
    for movie in movies_list:
        try:
            rating = float(movie.get("imdbRating", 0))
            sorted_movies.append((rating, movie))
        except (ValueError, TypeError):
            sorted_movies.append((0, movie))
    
    sorted_movies.sort(key=lambda x: x[0], reverse=True)
    
    # Group by primary genre
    for rating, movie in sorted_movies:
        genres = [g.strip() for g in movie.get("Genre", "").split(",") if g.strip()]
        if genres and movie["Title"] not in used_titles:
            primary_genre = genres[0]
            if len(genre_movies[primary_genre]) < max_per_genre:
                genre_movies[primary_genre].append(movie)
                used_titles.add(movie["Title"])
    
    return dict(genre_movies)