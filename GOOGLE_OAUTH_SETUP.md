# Google OAuth Setup Instructions

To enable Google OAuth authentication in your MovieHub application, follow these steps:

## 1. Create Google OAuth Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API (or Google OAuth 2.0)
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client IDs**
5. Set Application type to **Web application**
6. Add the following to **Authorized redirect URIs**:
   - `http://localhost:8000/auth/google/callback`
   - `http://127.0.0.1:8000/auth/google/callback`
7. For production, add your domain:
   - `https://yourdomain.com/auth/google/callback`

## 2. Configure Your Application

1. Copy your **Client ID** and **Client Secret** from Google Cloud Console
2. Open `oauth_config.py` in your project root
3. Replace the placeholder values:

```python
GOOGLE_CLIENT_ID = "your-actual-client-id.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-actual-client-secret"
```

## 3. Update Redirect URI for Production

If deploying to production, update the `OAUTH_REDIRECT_URI` in `oauth_config.py`:

```python
OAUTH_REDIRECT_URI = "https://yourdomain.com/auth/google/callback"
```

## 4. Test the Integration

1. Start your FastAPI server: `python main.py`
2. Go to `http://localhost:8000/login`
3. Click "Continue with Google"
4. You should be redirected to Google's authentication page
5. After successful authentication, you'll be redirected back to your app

## Features

- **Seamless Google Login**: Users can sign in with their Google accounts
- **Profile Information**: Displays user's name and profile picture
- **Dual Authentication**: Supports both Google OAuth and traditional email/password
- **Secure Sessions**: Uses secure session management
- **User Data Integration**: Google user data is stored and integrated with existing user system

## Security Notes

- Never commit your actual Google OAuth credentials to version control
- Use environment variables for production deployment
- Ensure HTTPS is enabled in production
- Regularly rotate your OAuth client secrets

## Troubleshooting

- **"OAuth callback error"**: Check that your redirect URI matches exactly
- **"Invalid client"**: Verify your Client ID and Secret are correct
- **"Access denied"**: Check that Google+ API is enabled in your Google Cloud project

## Environment Variables (Recommended for Production)

Instead of hardcoding credentials, use environment variables:

```python
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
```

Then set these in your deployment environment.
