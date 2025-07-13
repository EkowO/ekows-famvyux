from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from .utils import load_users, save_users, hash_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    username = request.session.get("username")
    # Check if Google OAuth is available
    try:
        import app.routes_google_auth
        google_oauth_available = True
    except ImportError:
        google_oauth_available = False
    
    return templates.TemplateResponse("register.html", {
        "request": request, 
        "error": None, 
        "username": username, 
        "search_query": "",
        "google_oauth_available": google_oauth_available
    })

@router.post("/register", response_class=HTMLResponse)
async def register(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    current_username = request.session.get("username")
    if username in users:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Username already exists.", "username": current_username, "search_query": ""})
    
    # Store user in new format to support both regular and OAuth users
    users[username] = {
        'password': hash_password(password),
        'email': username,  # Assume username is email for simplicity
        'name': username,
        'auth_type': 'regular'
    }
    save_users(users)
    request.session["username"] = username
    request.session["auth_type"] = "regular"
    return RedirectResponse(url="/", status_code=303)

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    username = request.session.get("username")
    error = request.query_params.get("error")
    
    # Check if Google OAuth is available
    try:
        import app.routes_google_auth
        google_oauth_available = True
    except ImportError:
        google_oauth_available = False
    
    # Handle OAuth error messages
    if error == "oauth_unavailable":
        error = "Google OAuth is not available. Please use email/password login."
    elif error == "oauth_failed":
        error = "Google authentication failed. Please try again."
    
    return templates.TemplateResponse("login.html", {
        "request": request, 
        "error": error, 
        "username": username, 
        "search_query": "",
        "google_oauth_available": google_oauth_available
    })

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    users = load_users()
    hashed = hash_password(password)
    current_username = request.session.get("username")
    
    if username not in users:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials.", "username": current_username, "search_query": ""})
    
    user = users[username]
    
    # Handle both old format (string) and new format (dict)
    if isinstance(user, str):
        # Old format: password is stored directly as string
        stored_password = user
    else:
        # New format: password is in dict
        stored_password = user.get('password')
        if not stored_password:
            return templates.TemplateResponse("login.html", {"request": request, "error": "This account uses Google login.", "username": current_username, "search_query": ""})
    
    if stored_password != hashed:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials.", "username": current_username, "search_query": ""})
    
    request.session["username"] = username
    request.session["auth_type"] = "regular"
    return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)