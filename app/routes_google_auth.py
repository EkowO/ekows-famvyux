from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import secrets
import sys
import os

# Add parent directory to path to import oauth_config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from authlib.integrations.starlette_client import OAuth
    from starlette.config import Config
    import httpx
    OAUTH_DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: OAuth dependencies not available: {e}")
    OAUTH_DEPENDENCIES_AVAILABLE = False
    # Create dummy classes to prevent import errors
    class OAuth:
        def __init__(self, config): pass
        def register(self, **kwargs): pass
    class Config:
        pass

try:
    from oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
except ImportError:
    # Fallback values if oauth_config is not properly set up
    GOOGLE_CLIENT_ID = "your-google-client-id.googleusercontent.com"
    GOOGLE_CLIENT_SECRET = "your-google-client-secret"
    OAUTH_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
    print("Warning: OAuth config not found. Please set up Google OAuth credentials in oauth_config.py")

from .utils import load_users, save_users

router = APIRouter()

# OAuth configuration - only if dependencies are available
if OAUTH_DEPENDENCIES_AVAILABLE:
    config = Config()
    oauth = OAuth(config)

    oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={
            'scope': 'openid email profile'
        }
    )
else:
    oauth = None

@router.get("/auth/google")
async def google_login(request: Request):
    """Initiate Google OAuth login"""
    if not OAUTH_DEPENDENCIES_AVAILABLE:
        return RedirectResponse(url="/login?error=oauth_unavailable", status_code=303)
    
    # Generate a random state for security
    state = secrets.token_urlsafe(32)
    request.session['oauth_state'] = state
    
    redirect_uri = OAUTH_REDIRECT_URI
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)

@router.get("/auth/google/callback")
async def google_callback(request: Request):
    """Handle Google OAuth callback"""
    if not OAUTH_DEPENDENCIES_AVAILABLE:
        return RedirectResponse(url="/login?error=oauth_unavailable", status_code=303)
    
    try:
        # Verify state parameter
        received_state = request.query_params.get('state')
        stored_state = request.session.get('oauth_state')
        
        if not received_state or received_state != stored_state:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        
        # Clear the state from session
        request.session.pop('oauth_state', None)
        
        # Get the token from Google
        token = await oauth.google.authorize_access_token(request)
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            # If userinfo is not in token, fetch it manually
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    'https://www.googleapis.com/oauth2/v2/userinfo',
                    headers={'Authorization': f'Bearer {token["access_token"]}'}
                )
                user_info = response.json()
        
        # Extract user information
        google_id = user_info.get('id')
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')
        
        if not email:
            raise HTTPException(status_code=400, detail="Could not get email from Google")
        
        # Load existing users
        users = load_users()
        
        # Create a username from email (use email as username for simplicity)
        username = email
        
        # Check if user already exists
        if username not in users:
            # Create new user
            users[username] = {
                'password': None,  # No password for OAuth users
                'google_id': google_id,
                'email': email,
                'name': name,
                'picture': picture,
                'auth_type': 'google'
            }
            save_users(users)
        else:
            # Update existing user with Google info
            if isinstance(users[username], str):
                # Old format user (just password), convert to new format
                users[username] = {
                    'password': users[username],
                    'google_id': google_id,
                    'email': email,
                    'name': name,
                    'picture': picture,
                    'auth_type': 'google'
                }
            else:
                # Update existing user
                users[username].update({
                    'google_id': google_id,
                    'email': email,
                    'name': name,
                    'picture': picture,
                    'auth_type': 'google'
                })
            save_users(users)
        
        # Set session
        request.session["username"] = username
        request.session["user_email"] = email
        request.session["user_name"] = name
        request.session["user_picture"] = picture
        request.session["auth_type"] = "google"
        
        # Redirect to home page
        return RedirectResponse(url="/", status_code=303)
        
    except Exception as e:
        print(f"OAuth callback error: {e}")
        # Redirect to login page with error
        return RedirectResponse(url="/login?error=oauth_failed", status_code=303)

@router.get("/auth/logout")
async def google_logout(request: Request):
    """Logout and clear session"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
