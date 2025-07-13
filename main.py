from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import SECRET_KEY
from app.routes_movies import router as movies_router
from app.routes_watch_later import router as watch_later_router
from app.routes_comments import router as comments_router
from app.routes_auth import router as auth_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(movies_router)
app.include_router(watch_later_router)
app.include_router(comments_router)
app.include_router(auth_router)

# Try to import Google OAuth router, make it optional
try:
    from app.routes_google_auth import router as google_auth_router
    app.include_router(google_auth_router)
    print("✅ Google OAuth authentication enabled")
except ImportError as e:
    print(f"⚠️  Google OAuth authentication disabled: {e}")
    print("   Install missing packages: pip install authlib httpx python-jose[cryptography]")