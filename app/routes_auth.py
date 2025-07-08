from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from .utils import load_users, save_users, hash_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})

@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    if username in users:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists."})
    users[username] = hash_password(password)
    save_users(users)
    request.session["username"] = username
    return RedirectResponse(url="/", status_code=303)

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    hashed = hash_password(password)
    if username not in users or users[username] != hashed:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})
    request.session["username"] = username
    return RedirectResponse(url="/", status_code=303)

@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)