import json
import hashlib
import os
from .config import MOVIES_FILE, LIKES_FILE, WATCH_LATER_FILE, USERS_FILE, COMMENTS_FILE

def load_movies():
    with open(MOVIES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

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