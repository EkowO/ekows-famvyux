#!/usr/bin/env python3

"""
Google OAuth Integration Test Script
This script verifies that the Google OAuth integration is properly set up.
"""

import sys
import os

def test_imports():
    """Test that all required packages are installed"""
    print("🔍 Testing imports...")
    
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
        
    try:
        import authlib
        print("✅ Authlib imported successfully")
    except ImportError as e:
        print(f"❌ Authlib import failed: {e}")
        return False
        
    try:
        import httpx
        print("✅ HTTPX imported successfully")
    except ImportError as e:
        print(f"❌ HTTPX import failed: {e}")
        return False
        
    return True

def test_oauth_config():
    """Test OAuth configuration"""
    print("\n🔍 Testing OAuth configuration...")
    
    try:
        from oauth_config import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_URI
        
        if GOOGLE_CLIENT_ID == "your-google-client-id.googleusercontent.com":
            print("⚠️  Google Client ID is still set to placeholder value")
            print("   Please update oauth_config.py with your actual Google OAuth credentials")
        else:
            print("✅ Google Client ID is configured")
            
        if GOOGLE_CLIENT_SECRET == "your-google-client-secret":
            print("⚠️  Google Client Secret is still set to placeholder value")
            print("   Please update oauth_config.py with your actual Google OAuth credentials")
        else:
            print("✅ Google Client Secret is configured")
            
        print(f"📍 OAuth Redirect URI: {OAUTH_REDIRECT_URI}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Could not import oauth_config: {e}")
        return False

def test_routes():
    """Test that routes can be imported"""
    print("\n🔍 Testing route imports...")
    
    try:
        from app.routes_google_auth import router
        print("✅ Google OAuth routes imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Google OAuth routes import failed: {e}")
        return False

def test_templates():
    """Test that templates exist"""
    print("\n🔍 Testing templates...")
    
    templates = [
        "templates/login.html",
        "templates/register.html",
        "templates/base.html"
    ]
    
    all_exist = True
    for template in templates:
        if os.path.exists(template):
            print(f"✅ {template} exists")
        else:
            print(f"❌ {template} not found")
            all_exist = False
            
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Google OAuth Integration Test\n")
    
    tests = [
        ("Package Imports", test_imports),
        ("OAuth Configuration", test_oauth_config),
        ("Route Imports", test_routes),
        ("Template Files", test_templates)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n📊 Test Results Summary:")
    print("=" * 40)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 40)
    
    if all_passed:
        print("🎉 All tests passed! Google OAuth integration is ready.")
        print("\n📋 Next Steps:")
        print("1. Set up Google OAuth credentials (see GOOGLE_OAUTH_SETUP.md)")
        print("2. Start the server: python main.py")
        print("3. Visit http://localhost:8000/login to test Google login")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("📖 See GOOGLE_OAUTH_SETUP.md for setup instructions.")

if __name__ == "__main__":
    main()
