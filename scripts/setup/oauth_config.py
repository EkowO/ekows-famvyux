# Google OAuth Configuration
# To get these credentials:
# 1. Go to https://console.developers.google.com/
# 2. Create a new project or select existing one
# 3. Enable Google+ API
# 4. Go to Credentials -> Create Credentials -> OAuth 2.0 Client IDs
# 5. Set Application type to "Web application"
# 6. Add authorized redirect URIs: http://localhost:8000/auth/google/callback
# 7. Copy Client ID and Client Secret here

GOOGLE_CLIENT_ID = "your-google-client-id.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-google-client-secret"

# For development, you can use these test values:
# Replace with your actual Google OAuth credentials when ready to deploy

# OAuth Settings
OAUTH_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
SECRET_KEY = "your-secret-key-change-this-in-production"
