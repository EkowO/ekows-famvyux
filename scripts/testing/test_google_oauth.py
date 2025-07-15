#!/usr/bin/env python3

"""
Quick Google OAuth Test
This script tests if Google OAuth is properly configured and working.
"""

import sys
import os

def test_oauth_config():
    """Test if OAuth configuration is properly set up"""
    print("🔍 Testing Google OAuth Configuration...")
    
    try:
        sys.path.append('.')
        from oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
        
        # Check if credentials are configured
        if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
            print("❌ Google Client ID is not configured")
            print("   Run: python setup_google_oauth.py")
            return False
            
        if GOOGLE_CLIENT_SECRET == "your-google-client-secret":
            print("❌ Google Client Secret is not configured")
            print("   Run: python setup_google_oauth.py")
            return False
        
        # Validate format
        if not GOOGLE_CLIENT_ID.endswith('.googleusercontent.com'):
            print("❌ Google Client ID format appears incorrect")
            print("   Should end with '.googleusercontent.com'")
            return False
            
        if len(GOOGLE_CLIENT_SECRET) < 10:
            print("❌ Google Client Secret appears too short")
            return False
        
        print("✅ OAuth credentials are configured")
        print(f"📧 Client ID: {GOOGLE_CLIENT_ID[:20]}...{GOOGLE_CLIENT_ID[-20:]}")
        print(f"🔐 Client Secret: {GOOGLE_CLIENT_SECRET[:8]}..." + "*" * 15)
        print(f"📍 Redirect URI: {OAUTH_REDIRECT_URI}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Could not import oauth_config: {e}")
        print("   Run: python setup_google_oauth.py")
        return False
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_oauth_dependencies():
    """Test if OAuth dependencies are installed"""
    print("\n🔍 Testing OAuth Dependencies...")
    
    try:
        import authlib
        print("✅ authlib installed")
    except ImportError:
        print("❌ authlib not installed")
        print("   Run: pip install authlib")
        return False
    
    try:
        import httpx
        print("✅ httpx installed")
    except ImportError:
        print("❌ httpx not installed")
        print("   Run: pip install httpx")
        return False
        
    try:
        from jose import jwt
        print("✅ python-jose installed")
    except ImportError:
        print("❌ python-jose not installed")
        print("   Run: pip install python-jose[cryptography]")
        return False
    
    return True

def test_server_import():
    """Test if the server can be imported without errors"""
    print("\n🔍 Testing Server Import...")
    
    try:
        import main
        print("✅ Server imports successfully")
        return True
    except Exception as e:
        print(f"❌ Server import failed: {e}")
        return False

def test_oauth_routes():
    """Test if OAuth routes are accessible"""
    print("\n🔍 Testing OAuth Routes...")
    
    try:
        from app.routes_google_auth import router
        print("✅ Google OAuth routes loaded")
        
        # Check if routes are registered
        route_paths = [route.path for route in router.routes]
        
        if "/auth/google" in route_paths:
            print("✅ Google login route available")
        else:
            print("❌ Google login route not found")
            return False
            
        if "/auth/google/callback" in route_paths:
            print("✅ Google callback route available")
        else:
            print("❌ Google callback route not found")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ OAuth routes test failed: {e}")
        return False

def main():
    """Run all OAuth tests"""
    print("🧪 Google OAuth Integration Test")
    print("=" * 40)
    
    tests = [
        ("OAuth Configuration", test_oauth_config),
        ("OAuth Dependencies", test_oauth_dependencies),
        ("Server Import", test_server_import),
        ("OAuth Routes", test_oauth_routes)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! Google OAuth is ready to use.")
        print("\n🚀 Next Steps:")
        print("1. Start server: python start_server.py")
        print("2. Open browser: http://localhost:8000/login")
        print("3. Click 'Continue with Google'")
        print("4. Test the authentication flow")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print("\n🔧 Common Solutions:")
        print("- Run setup: python setup_google_oauth.py")
        print("- Install dependencies: pip install authlib httpx python-jose[cryptography]")
        print("- Check Google Cloud Console settings")

if __name__ == "__main__":
    main()
