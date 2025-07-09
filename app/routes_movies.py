from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .utils import (
    load_movies, save_movies, load_likes, save_likes,
    get_all_unique_movies, get_child_unique_movies,
    get_final_top_movies_by_genre, search_movies
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, q: str = ""):
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    child_unique_movies = get_child_unique_movies(movies)
    final_top_movies_by_genre = get_final_top_movies_by_genre(child_unique_movies)
    username = request.session.get("username")
    
    if q:
        found_movies = search_movies(q, all_unique_movies)
        return templates.TemplateResponse(
            "search_results.html",
            {"request": request, "found_movies": found_movies, "search_query": q, "username": username}
        )
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "username": username, "top_movies_by_genre": final_top_movies_by_genre, "search_query": q}
    )

@router.get("/movie/{imdb_id}", response_class=HTMLResponse)
async def movie_detail(request: Request, imdb_id: str):
    movies = load_movies()
    movie = next((m for m in movies if str(m.get('imdbID')) == str(imdb_id)), None)
    if not movie:
        return templates.TemplateResponse("movie_not_found.html", {"request": request}, status_code=404)
    from .utils import load_comments
    comments = load_comments()
    movie_comments = comments.get(imdb_id, [])
    username = request.session.get("username")
    return templates.TemplateResponse(
        "movie_detail.html",
        {
            "request": request,
            "movie": movie,
            "comments": movie_comments,
            "username": username,
            "search_query": ""
        }
    )

@router.post("/like/{imdb_id}")
async def like_movie(request: Request, imdb_id: str):
    likes = load_likes()
    likes[imdb_id] = likes.get(imdb_id, 0) + 1
    save_likes(likes)
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=303)

@router.get("/add", response_class=HTMLResponse)
async def add_movie_form(request: Request):
    return templates.TemplateResponse("add_movie.html", {"request": request, "error": None})

@router.post("/add", response_class=HTMLResponse)
async def add_movie(
    request: Request,
    title: str = Form(...),
    description: str = Form("")
):
    movies = load_movies()
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

@router.post("/save_movie")
async def save_movie(movie_id: str = Form(...)):
    likes = load_likes()
    if isinstance(likes, list):
        likes = {mid: 1 for mid in likes}
    likes[movie_id] = likes.get(movie_id, 0) + 1
    save_likes(likes)
    return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)

@router.get("/saved", response_class=HTMLResponse)
async def show_saved_movies(request: Request):
    likes = load_likes()
    saved_ids = set(likes.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    saved_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in saved_ids]
    return templates.TemplateResponse(
        "saved_movies.html",
        {"request": request, "saved_movies": saved_movies}
    )

@router.get("/liked", response_class=HTMLResponse)
async def view_liked_movies(request: Request):
    likes = load_likes()
    liked_ids = set(likes.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    liked_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in liked_ids]
    username = request.session.get("username")
    return templates.TemplateResponse(
        "liked_movies.html",
        {"request": request, "liked_movies": liked_movies, "username": username, "search_query": ""}
    )