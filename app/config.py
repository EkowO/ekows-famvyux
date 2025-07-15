import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIKES_FILE = os.path.join(BASE_DIR, 'data', 'get movies', 'movie_likes.json')
MOVIES_FILE = os.path.join(BASE_DIR, 'data', 'get movies', 'all_10000_movies.json')
WATCH_LATER_FILE = os.path.join(BASE_DIR, 'data', 'get movies', 'watch_later.json')
USERS_FILE = os.path.join(BASE_DIR, 'data', 'get movies', 'users.json')
COMMENTS_FILE = os.path.join(BASE_DIR, 'data', 'get movies', 'comments.json')
SECRET_KEY = "your-secret-key"  # Change this to a random string!