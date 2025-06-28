import os
import json
import hashlib
from collections import defaultdict
from fastapi import FastAPI, Request, Form, Response, status, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from itsdangerous import URLSafeSerializer
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LIKES_FILE = os.path.join(BASE_DIR, 'get movies', 'movie_likes.json')
MOVIES_FILE = os.path.join(BASE_DIR, 'get movies', 'all_10000_movies.json')
WATCH_LATER_FILE = os.path.join(BASE_DIR, 'get movies', 'watch_later.json')
USERS_FILE = os.path.join(BASE_DIR, 'get movies', 'users.json')
SECRET_KEY = "your-secret-key"  # Change this to a random string!
serializer = URLSafeSerializer(SECRET_KEY)

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

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# --- Remove duplicates by title (all movies, for search) ---
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

# --- Remove duplicates and filter for child-appropriate content (for genre display) ---
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
        # Only include movies with a valid float imdbRating
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

# --- Search Functionality (searches all movies, not just child-appropriate) ---
def search_movies(query, all_unique_movies):
    query = query.lower().strip()
    found_movies = []
    for m in all_unique_movies.values():
        if query in m.get("Title", "").lower():
            found_movies.append(m)
    return found_movies

# --- FastAPI Routes ---
@app.get("/", response_class=HTMLResponse)
async def home(request: Request, q: str = ""):
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    child_unique_movies = get_child_unique_movies(movies)
    final_top_movies_by_genre = get_final_top_movies_by_genre(child_unique_movies)
    if q:
        found_movies = search_movies(q, all_unique_movies)
        return templates.TemplateResponse(
            "search_results.html",
            {"request": request, "found_movies": found_movies, "search_query": q}
        )
    username = request.session.get("username") if "session" in request.scope else None
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": username, "top_movies_by_genre": final_top_movies_by_genre, "search_query": ""}
    )

@app.get("/movie/{imdb_id}", response_class=HTMLResponse)
async def movie_detail(request: Request, imdb_id: str):
    import os, json
    # Load movies
    with open(os.path.join("get movies", "all_10000_movies.json")) as f:
        movies = json.load(f)
    movie = next((m for m in movies if str(m.get('imdbID')) == str(imdb_id)), None)
    if not movie:
        return templates.TemplateResponse("movie_not_found.html", {"request": request}, status_code=404)

    comments = load_comments()
    movie_comments = comments.get(imdb_id, [])

    username = request.session.get("username") if "session" in request.scope else None

    return templates.TemplateResponse(
        "movie_detail.html",
        {
            "request": request,
            "movie": movie,
            "comments": movie_comments,
            "username": username,
        }
    )

@app.post("/like/{imdb_id}")
async def like_movie(request: Request, imdb_id: str):
    likes = load_likes()
    likes[imdb_id] = likes.get(imdb_id, 0) + 1
    save_likes(likes)
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=303)

@app.get("/add", response_class=HTMLResponse)
async def add_movie_form(request: Request):
    return templates.TemplateResponse("add_movie.html", {"request": request, "error": None})

@app.post("/add", response_class=HTMLResponse)
async def add_movie(
    request: Request,
    title: str = Form(...),
    description: str = Form("")
):
    movies = load_movies()
    # Generate a new unique ID (use max imdbID or fallback to 0)
    existing_ids = [int(m.get("imdbID", "0").replace("tt", "")) for m in movies if m.get("imdbID", "").replace("tt", "").isdigit()]
    new_id_num = max(existing_ids + [0]) + 1
    new_imdb_id = f"tt{new_id_num:07d}"
    if title:
        new_movie = {
            "imdbID": new_imdb_id,
            "Title": title,
            "description": description,
            "imdbRating": "N/A",
            "Poster": "",
            "Rated": "",
            "Genre": ""
        }
        movies.append(new_movie)
        save_movies(movies)
        return RedirectResponse(url=f"/movie/{new_imdb_id}", status_code=303)
    else:
        return templates.TemplateResponse("add_movie.html", {"request": request, "error": "Title is required."})

@app.post("/save_movie")
async def save_movie(movie_id: str = Form(...)):
    likes = load_likes()
    if isinstance(likes, list):
        # Convert old list format to dict
        likes = {mid: 1 for mid in likes}
    likes[movie_id] = likes.get(movie_id, 0) + 1
    save_likes(likes)
    return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)

@app.get("/saved", response_class=HTMLResponse)
async def show_saved_movies(request: Request):
    likes = load_likes()  # This is a dict: {imdb_id: count}
    saved_ids = set(likes.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    saved_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in saved_ids]
    return templates.TemplateResponse(
        "saved_movies.html",
        {"request": request, "saved_movies": saved_movies}
    )

@app.get("/liked", response_class=HTMLResponse)
async def view_liked_movies(request: Request):
    likes = load_likes()  # {imdb_id: count}
    liked_ids = set(likes.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    liked_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in liked_ids]
    return templates.TemplateResponse(
        "liked_movies.html",
        {"request": request, "liked_movies": liked_movies}
    )

@app.post("/watch_later/{imdb_id}")
async def watch_later_movie(request: Request, imdb_id: str):
    watch_later = load_watch_later()
    watch_later[imdb_id] = True
    save_watch_later(watch_later)
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=303)

@app.post("/remove_watch_later/{imdb_id}")
async def remove_watch_later(imdb_id: str):
    watch_later = load_watch_later()
    if imdb_id in watch_later:
        del watch_later[imdb_id]
        save_watch_later(watch_later)
    return RedirectResponse(url="/watch_later", status_code=303)

@app.get("/watch_later", response_class=HTMLResponse)
async def view_watch_later(request: Request):
    watch_later = load_watch_later()
    watch_later_ids = set(watch_later.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    watch_later_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in watch_later_ids]
    return templates.TemplateResponse(
        "watch_later.html",
        {"request": request, "watch_later_movies": watch_later_movies}
    )

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@app.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists."})
    users[username] = hash_password(password)
    save_users(users)
    response = RedirectResponse(url="/login", status_code=303)
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username not in users or users[username] != hash_password(password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})
    # Set a signed cookie
    session_token = serializer.dumps({"username": username})
    resp = RedirectResponse(url="/", status_code=303)
    resp.set_cookie("session", session_token, httponly=True)
    return resp

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

def get_current_user(session: str = Cookie(None)):
    if not session:
        return None
    try:
        data = serializer.loads(session)
        return data.get("username")
    except Exception:
        return None

@app.post("/remove_liked/{imdb_id}")
async def remove_liked(imdb_id: str):
    likes = load_likes()
    if imdb_id in likes:
        del likes[imdb_id]
        save_likes(likes)
    return RedirectResponse(url="/liked", status_code=303)

def load_comments():
    path = os.path.join("get movies", "comments.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_comments(comments):
    path = os.path.join("get movies", "comments.json")
    with open(path, "w") as f:
        json.dump(comments, f, indent=2)

@app.post("/movie/{movie_id}/comment")
async def add_comment(request: Request, movie_id: str, comment: str = Form(...)):
    # Load comments
    import os, json
    comments_path = os.path.join("get movies", "comments.json")
    if os.path.exists(comments_path):
        with open(comments_path, "r") as f:
            comments = json.load(f)
    else:
        comments = {}

    # Get username from session (if using sessions)
    username = request.session.get("username") if "session" in request.scope else None
    if not username:
        return RedirectResponse(url="/login", status_code=303)

    # Add the comment
    movie_comments = comments.get(movie_id, [])
    movie_comments.append({"user": username, "text": comment})
    comments[movie_id] = movie_comments

    # Save comments
    with open(comments_path, "w") as f:
        json.dump(comments, f, indent=2)

    return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)