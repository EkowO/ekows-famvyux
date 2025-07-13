#!/usr/bin/env python3

"""
Google OAuth Setup for MovieHub
This script helps configure Google OAuth authentication
"""

import os
import json

def setup_google_oauth():
    """Set up Google OAuth configuration"""
    
    print("🔐 Google OAuth Setup for MovieHub")
    print("=" * 50)
    
    print("\n📋 To enable Google sign-in, you need to:")
    print("1. Go to Google Cloud Console: https://console.cloud.google.com/")
    print("2. Create a new project or select an existing one")
    print("3. Enable the Google+ API and Google OAuth2 API")
    print("4. Go to 'Credentials' -> 'Create Credentials' -> 'OAuth 2.0 Client IDs'")
    print("5. Set Application type to 'Web application'")
    print("6. Add these authorized redirect URIs:")
    print("   - http://localhost:8000/auth/google/callback")
    print("   - http://127.0.0.1:8000/auth/google/callback")
    print("7. Copy the Client ID and Client Secret")
    
    print("\n🔧 Current OAuth Configuration:")
    
    # Check if oauth_config.py exists and has proper values
    try:
        import sys
        sys.path.append('.')
        from oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
        
        if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
            print("   ❌ Google Client ID: Not configured (using placeholder)")
        else:
            print(f"   ✅ Google Client ID: {GOOGLE_CLIENT_ID[:20]}...")
            
        if GOOGLE_CLIENT_SECRET == "your-google-client-secret":
            print("   ❌ Google Client Secret: Not configured (using placeholder)")
        else:
            print("   ✅ Google Client Secret: Configured")
            
        print(f"   ✅ Redirect URI: {OAUTH_REDIRECT_URI}")
        
    except ImportError:
        print("   ❌ oauth_config.py: Not found or has errors")
    
    # Check dependencies
    print("\n📦 Dependencies:")
    try:
        import authlib
        print(f"   ✅ authlib: {authlib.__version__}")
    except ImportError:
        print("   ❌ authlib: Not installed")
        
    try:
        import httpx
        print(f"   ✅ httpx: {httpx.__version__}")
    except ImportError:
        print("   ❌ httpx: Not installed")
    
    # Check route availability
    print("\n🛤️  Routes:")
    try:
        from app.routes_google_auth import router
        print("   ✅ Google OAuth routes: Available")
    except ImportError as e:
        print(f"   ❌ Google OAuth routes: Error - {e}")
    
    # Create a sample configuration
    sample_config = '''# Google OAuth Configuration for MovieHub
# Replace the placeholder values below with your actual Google OAuth credentials

# From Google Cloud Console -> Credentials -> OAuth 2.0 Client IDs
GOOGLE_CLIENT_ID = "your-actual-client-id.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "your-actual-client-secret"

# OAuth Settings (these should work for local development)
OAUTH_REDIRECT_URI = "http://localhost:8000/auth/google/callback"
SECRET_KEY = "your-secret-key-change-this-in-production"

# For production, also set:
# OAUTH_REDIRECT_URI = "https://yourdomain.com/auth/google/callback"
'''
    
    with open("oauth_config_sample.py", "w") as f:
        f.write(sample_config)
    
    print("\n💡 Next Steps:")
    
    # Check if dependencies are missing
    missing_deps = []
    try:
        import authlib
    except ImportError:
        missing_deps.append("authlib")
        
    try:
        import httpx
    except ImportError:
        missing_deps.append("httpx")
    
    if missing_deps:
        print(f"   1. Install missing dependencies: pip install {' '.join(missing_deps)}")
    else:
        print("   1. ✅ All dependencies are installed")
    
    if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
        print("   2. Update oauth_config.py with your Google OAuth credentials")
        print("      (See oauth_config_sample.py for the format)")
    else:
        print("   2. ✅ Google OAuth credentials are configured")
    
    print("   3. Start the server: python final_server.py")
    print("   4. Visit: http://localhost:8000/login")
    print("   5. Click 'Continue with Google' to test")
    
    print("\n🧪 Testing OAuth Setup:")
    
    # Test if everything would work
    all_good = True
    
    if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
        print("   ❌ Need to configure Google Client ID")
        all_good = False
    
    if GOOGLE_CLIENT_SECRET == "your-google-client-secret":
        print("   ❌ Need to configure Google Client Secret")
        all_good = False
    
    try:
        import authlib
        import httpx
    except ImportError:
        print("   ❌ Missing required dependencies")
        all_good = False
    
    if all_good:
        print("   🎉 Google OAuth should work! Test it by starting the server.")
    else:
        print("   ⚠️  Complete the setup steps above first.")
    
    return all_good

if __name__ == "__main__":
    setup_google_oauth()
