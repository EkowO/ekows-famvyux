from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from .utils import load_watch_later, save_watch_later, load_movies, get_all_unique_movies

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/watch_later/{imdb_id}")
async def watch_later_movie(request: Request, imdb_id: str):
    watch_later = load_watch_later()
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    user_list = watch_later.get(username, [])
    if imdb_id not in user_list:
        user_list.append(imdb_id)
    watch_later[username] = user_list
    save_watch_later(watch_later)
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=303)

@router.post("/remove_watch_later/{imdb_id}")
async def remove_watch_later(request: Request, imdb_id: str):
    watch_later = load_watch_later()
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    user_list = watch_later.get(username, [])
    if imdb_id in user_list:
        user_list.remove(imdb_id)
    watch_later[username] = user_list
    save_watch_later(watch_later)
    referer = request.headers.get("referer") or "/"
    return RedirectResponse(url=referer, status_code=303)

@router.get("/watch_later", response_class=HTMLResponse)
async def show_watch_later(
    request: Request,
    genre: str = "", 
    min_rating: str = "", 
    max_rating: str = "",
    year_from: str = "", 
    year_to: str = "",
    rated: str = ""
):
    watch_later = load_watch_later()
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    
    user_list = watch_later.get(username, [])
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    watch_later_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in user_list]
    
    # Get filter options
    from .utils import get_filter_options, filter_movies
    filter_options = get_filter_options(all_unique_movies)
    
    # Convert string parameters to proper types
    min_rating_val = None
    max_rating_val = None
    year_from_val = None
    year_to_val = None
    
    try:
        if min_rating.strip():
            min_rating_val = float(min_rating)
    except (ValueError, AttributeError):
        pass
    
    try:
        if max_rating.strip():
            max_rating_val = float(max_rating)
    except (ValueError, AttributeError):
        pass
    
    try:
        if year_from.strip():
            year_from_val = int(year_from)
    except (ValueError, AttributeError):
        pass
    
    try:
        if year_to.strip():
            year_to_val = int(year_to)
    except (ValueError, AttributeError):
        pass
    
    # Apply filters to watch later movies
    if any([genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated]):
        filtered_watch_later_movies = filter_movies(
            {m["imdbID"]: m for m in watch_later_movies}, "", genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated
        )
        watch_later_movies = list(filtered_watch_later_movies)
    
    return templates.TemplateResponse(
        "watch_later.html",
        {
            "request": request, 
            "watch_later_movies": watch_later_movies, 
            "username": username, 
            "search_query": "",
            "filter_options": filter_options,
            "current_filters": {
                "genre": genre, "min_rating": min_rating, "max_rating": max_rating,
                "year_from": year_from, "year_to": year_to, "rated": rated
            }
        }
    )