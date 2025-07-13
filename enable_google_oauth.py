#!/usr/bin/env python3

"""
Enable Google OAuth - Complete Setup
This script tests and helps set up Google OAuth for MovieHub
"""

def check_google_oauth_status():
    """Check current Google OAuth status and provide setup guidance"""
    
    print("🔐 Google OAuth Setup for MovieHub")
    print("=" * 60)
    
    # Check 1: Dependencies
    print("\n📦 Checking Dependencies...")
    dependencies_ok = True
    
    try:
        import authlib
        print(f"   ✅ authlib: {authlib.__version__}")
    except ImportError:
        print("   ❌ authlib: Not installed")
        dependencies_ok = False
    
    try:
        import httpx
        print(f"   ✅ httpx: {httpx.__version__}")
    except ImportError:
        print("   ❌ httpx: Not installed") 
        dependencies_ok = False
        
    try:
        from jose import jwt
        print("   ✅ python-jose: Available")
    except ImportError:
        print("   ❌ python-jose: Not installed")
        dependencies_ok = False
    
    # Check 2: Configuration
    print("\n🔧 Checking Configuration...")
    config_ok = True
    
    try:
        from oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
        
        if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
            print("   ❌ Google Client ID: Using placeholder (needs real credentials)")
            config_ok = False
        else:
            print(f"   ✅ Google Client ID: {GOOGLE_CLIENT_ID[:25]}...")
            
        if GOOGLE_CLIENT_SECRET == "your-google-client-secret":
            print("   ❌ Google Client Secret: Using placeholder (needs real credentials)")
            config_ok = False
        else:
            print("   ✅ Google Client Secret: Configured")
            
        print(f"   ✅ Redirect URI: {OAUTH_REDIRECT_URI}")
        
    except ImportError:
        print("   ❌ oauth_config.py: Missing or has errors")
        config_ok = False
    
    # Check 3: Routes
    print("\n🛤️  Checking Routes...")
    routes_ok = True
    
    try:
        from app.routes_google_auth import router, OAUTH_DEPENDENCIES_AVAILABLE
        print("   ✅ Google OAuth router: Available")
        
        if OAUTH_DEPENDENCIES_AVAILABLE:
            print("   ✅ OAuth dependencies: Loaded successfully")
        else:
            print("   ❌ OAuth dependencies: Failed to load")
            routes_ok = False
            
    except ImportError as e:
        print(f"   ❌ Google OAuth router: Import failed - {e}")
        routes_ok = False
    
    # Check 4: Main app integration
    print("\n🔗 Checking Main App Integration...")
    app_ok = True
    
    try:
        # Import main app (this will trigger the OAuth router inclusion)
        import io
        import contextlib
        
        # Capture output from main.py imports
        output_capture = io.StringIO()
        with contextlib.redirect_stdout(output_capture):
            from main import app
        
        output = output_capture.getvalue()
        
        if "Google OAuth authentication enabled" in output:
            print("   ✅ Google OAuth: Successfully enabled in main app")
        elif "Google OAuth authentication disabled" in output:
            print("   ⚠️  Google OAuth: Disabled in main app (check dependencies)")
            app_ok = False
        else:
            print("   ✅ Main app: Loaded successfully")
            
    except Exception as e:
        print(f"   ❌ Main app: Error loading - {e}")
        app_ok = False
    
    # Overall status
    print("\n" + "=" * 60)
    
    overall_status = dependencies_ok and config_ok and routes_ok and app_ok
    
    if overall_status:
        print("🎉 GOOGLE OAUTH IS READY!")
        print("\n✅ Next Steps:")
        print("   1. Start the server: python final_server.py")
        print("   2. Open: http://localhost:8000/login")
        print("   3. Click 'Continue with Google' to test")
        print("   4. You should be redirected to Google for authentication")
        
    else:
        print("⚠️  GOOGLE OAUTH NEEDS SETUP")
        print("\n🛠️  Required Actions:")
        
        if not dependencies_ok:
            print("   1. Install dependencies:")
            print("      pip install authlib httpx python-jose[cryptography]")
        
        if not config_ok:
            print("   2. Set up Google OAuth credentials:")
            print("      a. Go to: https://console.cloud.google.com/")
            print("      b. Create/select a project")
            print("      c. Enable Google OAuth2 API")
            print("      d. Create OAuth 2.0 Client ID")
            print("      e. Add redirect URI: http://localhost:8000/auth/google/callback")
            print("      f. Update oauth_config.py with your Client ID and Secret")
        
        if not routes_ok:
            print("   3. Fix route issues (usually dependency-related)")
        
        if not app_ok:
            print("   4. Check main app configuration")
    
    print("\n📖 Detailed Setup Guide:")
    print("   See: GOOGLE_OAUTH_SETUP.md")
    
    return overall_status

def create_setup_guide():
    """Create a detailed setup guide"""
    
    guide_content = """# Google OAuth Setup Guide for MovieHub

## Prerequisites
- Python 3.7+
- pip package manager
- Google account

## Step 1: Install Dependencies
```bash
pip install authlib httpx python-jose[cryptography]
```

## Step 2: Set Up Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Click "Select a project" at the top
   - Create a new project or choose an existing one

3. **Enable APIs**
   - Go to "APIs & Services" > "Library"
   - Search for and enable:
     - Google+ API
     - Google OAuth2 API

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth 2.0 Client ID"
   - Choose "Web application"
   - Set these authorized redirect URIs:
     ```
     http://localhost:8000/auth/google/callback
     http://127.0.0.1:8000/auth/google/callback
     ```
   - Click "Create"
   - Copy the Client ID and Client Secret

## Step 3: Configure MovieHub

1. **Update oauth_config.py**
   Replace the placeholder values with your actual credentials:
   ```python
   GOOGLE_CLIENT_ID = "your-actual-client-id.googleusercontent.com"
   GOOGLE_CLIENT_SECRET = "your-actual-client-secret"
   OAUTH_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
   ```

## Step 4: Test the Setup

1. **Run the test script**
   ```bash
   python enable_google_oauth.py
   ```

2. **Start the server**
   ```bash
   python final_server.py
   ```

3. **Test login**
   - Open: http://localhost:8000/login
   - Click "Continue with Google"
   - You should be redirected to Google for authentication

## Troubleshooting

### Common Issues:

1. **"OAuth dependencies not available"**
   - Install missing packages: `pip install authlib httpx python-jose[cryptography]`

2. **"Google Client ID is not configured"**
   - Update oauth_config.py with real credentials from Google Cloud Console

3. **"Redirect URI mismatch"**
   - Make sure the redirect URI in Google Cloud Console matches exactly:
     `http://localhost:8000/auth/google/callback`

4. **Server won't start**
   - Check if port 8000 is already in use
   - Try a different port by modifying the server script

### For Production:

1. Update the redirect URI to your domain:
   ```python
   OAUTH_REDIRECT_URI = "https://yourdomain.com/auth/google/callback"
   ```

2. Add your production domain to Google Cloud Console redirect URIs

3. Use environment variables for credentials instead of hardcoding them

## Security Notes

- Never commit real OAuth credentials to version control
- Use environment variables for production credentials
- Regularly rotate your OAuth secrets
- Only add trusted redirect URIs in Google Cloud Console

## Features Enabled

Once Google OAuth is set up, users can:
- Sign in with their Google account
- Automatic account creation for new users
- Profile information from Google (name, email, profile picture)
- Session management across the application
- Secure logout functionality
"""
    
    with open("GOOGLE_OAUTH_SETUP.md", "w") as f:
        f.write(guide_content)
    
    print("📖 Created detailed setup guide: GOOGLE_OAUTH_SETUP.md")

if __name__ == "__main__":
    print("🚀 MovieHub Google OAuth Setup\n")
    
    # Create the setup guide
    create_setup_guide()
    
    # Check current status
    status = check_google_oauth_status()
    
    if not status:
        print("\n💡 Quick Start:")
        print("   1. pip install authlib httpx python-jose[cryptography]")
        print("   2. Get Google OAuth credentials from Google Cloud Console")
        print("   3. Update oauth_config.py with your credentials")
        print("   4. Run this script again to verify")
        print("   5. Start the server and test at http://localhost:8000/login")
