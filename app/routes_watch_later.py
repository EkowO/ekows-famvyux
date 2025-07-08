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
async def show_watch_later(request: Request):
    watch_later = load_watch_later()
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    user_list = watch_later.get(username, [])
    movies = load_movies()
    all_unique_movies = get_all_unique_movies(movies)
    watch_later_movies = [m for m in all_unique_movies.values() if m.get("imdbID") in user_list]
    return templates.TemplateResponse(
        "watch_later.html",
        {"request": request, "watch_later_movies": watch_later_movies}
    )