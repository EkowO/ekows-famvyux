from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from .utils import (
    load_movies, save_movies, load_likes, save_likes,
    get_all_unique_movies, get_child_unique_movies,
    get_final_top_movies_by_genre, search_movies,
    filter_movies, get_filter_options, organize_movies_by_genre
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(
    request: Request, 
    q: str = "", 
    genre: str = "", 
    min_rating: str = "", 
    max_rating: str = "",
    year_from: str = "", 
    year_to: str = "",
    rated: str = ""
):
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    child_unique_movies = get_child_unique_movies(movies)
    username = request.session.get("username")
    
    # Get all available filter options
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
    
    # Apply filters if any are specified
    if any([q, genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated]):
        filtered_movies = filter_movies(
            all_unique_movies, q, genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated
        )
        
        if q:  # If there's a search query, show search results template
            return templates.TemplateResponse(
                "search_results.html",
                {
                    "request": request, 
                    "found_movies": filtered_movies, 
                    "search_query": q, 
                    "username": username,
                    "filter_options": filter_options,
                    "current_filters": {
                        "genre": genre, "min_rating": min_rating, "max_rating": max_rating,
                        "year_from": year_from, "year_to": year_to, "rated": rated
                    }
                }
            )
        else:  # Show filtered results on main page
            # Organize filtered movies by genre for display
            filtered_by_genre = organize_movies_by_genre(filtered_movies)
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request, 
                    "username": username, 
                    "top_movies_by_genre": filtered_by_genre, 
                    "search_query": q,
                    "filter_options": filter_options,
                    "current_filters": {
                        "genre": genre, "min_rating": min_rating, "max_rating": max_rating,
                        "year_from": year_from, "year_to": year_to, "rated": rated
                    },
                    "is_filtered": True
                }
            )
    
    # Default view - show top movies by genre
    final_top_movies_by_genre = get_final_top_movies_by_genre(child_unique_movies)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request, 
            "username": username, 
            "top_movies_by_genre": final_top_movies_by_genre, 
            "search_query": q,
            "filter_options": filter_options,
            "current_filters": {},
            "is_filtered": False
        }
    )

@router.get("/movie/{imdb_id}", response_class=HTMLResponse)
async def movie_detail(request: Request, imdb_id: str):
    movies = load_movies()
    movie = next((m for m in movies if str(m.get('imdbID')) == str(imdb_id)), None)
    if not movie:
        username = request.session.get("username")
        return templates.TemplateResponse("movie_not_found.html", {"request": request, "username": username, "search_query": ""}, status_code=404)
    from .utils import load_comments, format_timestamp
    comments = load_comments()
    movie_comments = comments.get(imdb_id, [])
    
    # Format timestamps for display
    for comment in movie_comments:
        if 'timestamp' in comment:
            comment['formatted_timestamp'] = format_timestamp(comment['timestamp'])
    
    # Check if movie is liked
    likes = load_likes()
    is_liked = imdb_id in likes
    
    username = request.session.get("username")
    return templates.TemplateResponse(
        "movie_detail.html",
        {
            "request": request,
            "movie": movie,
            "comments": movie_comments,
            "username": username,
            "search_query": "",
            "is_liked": is_liked
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
async def view_liked_movies(
    request: Request,
    genre: str = "", 
    min_rating: str = "", 
    max_rating: str = "",
    year_from: str = "", 
    year_to: str = "",
    rated: str = ""
):
    likes = load_likes()
    liked_ids = set(likes.keys())
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    liked_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in liked_ids]
    username = request.session.get("username")
    
    # Get filter options
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
    
    # Apply filters to liked movies
    if any([genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated]):
        filtered_liked_movies = filter_movies(
            {m["imdbID"]: m for m in liked_movies}, "", genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated
        )
        liked_movies = list(filtered_liked_movies)
    
    return templates.TemplateResponse(
        "liked_movies.html",
        {
            "request": request, 
            "liked_movies": liked_movies, 
            "username": username, 
            "search_query": "",
            "filter_options": filter_options,
            "current_filters": {
                "genre": genre, "min_rating": min_rating, "max_rating": max_rating,
                "year_from": year_from, "year_to": year_to, "rated": rated
            }
        }
    )

@router.post("/remove_liked/{movie_id}")
async def remove_liked_movie(request: Request, movie_id: str):
    """Remove a movie from the liked movies list"""
    likes = load_likes()
    if movie_id in likes:
        del likes[movie_id]
        save_likes(likes)
    return RedirectResponse(url="/liked", status_code=303)

@router.get("/browse", response_class=HTMLResponse)
async def browse_movies(
    request: Request, 
    genre: str = "", 
    min_rating: str = "", 
    max_rating: str = "",
    year_from: str = "", 
    year_to: str = "",
    rated: str = "",
    sort_by: str = "rating"
):
    """Browse movies with advanced filtering options"""
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    username = request.session.get("username")
    
    # Get all available filter options
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
    
    # Apply filters
    filtered_movies = filter_movies(
        all_unique_movies, "", genre, min_rating_val, max_rating_val, year_from_val, year_to_val, rated
    )
    
    # Sort movies
    if sort_by == "rating":
        filtered_movies.sort(key=lambda x: float(x.get("imdbRating", 0)), reverse=True)
    elif sort_by == "year":
        filtered_movies.sort(key=lambda x: int(x.get("Year", 0)), reverse=True)
    elif sort_by == "title":
        filtered_movies.sort(key=lambda x: x.get("Title", ""))
    
    return templates.TemplateResponse(
        "browse_movies.html",
        {
            "request": request, 
            "movies": filtered_movies,
            "username": username,
            "filter_options": filter_options,
            "current_filters": {
                "genre": genre, "min_rating": min_rating, "max_rating": max_rating,
                "year_from": year_from, "year_to": year_to, "rated": rated, "sort_by": sort_by
            },
            "search_query": ""
        }
    )