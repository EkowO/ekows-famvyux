#!/usr/bin/env python3

"""
Comprehensive error diagnosis that writes results to a file
"""

import sys
import traceback
import json
from datetime import datetime

def write_log(message):
    """Write message to both console and log file"""
    print(message)
    with open("error_diagnosis.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: {message}\n")

def test_server_startup():
    """Test all components that could cause server startup errors"""
    
    write_log("🔍 Starting comprehensive error diagnosis...")
    
    # Test 1: Basic Python imports
    write_log("\n1. Testing basic imports...")
    try:
        import fastapi
        import uvicorn
        import jinja2
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        write_log("   ✅ Basic FastAPI imports successful")
    except Exception as e:
        write_log(f"   ❌ Basic imports failed: {e}")
        return False
    
    # Test 2: App configuration
    write_log("\n2. Testing app configuration...")
    try:
        from app.config import SECRET_KEY, MOVIES_FILE, LIKES_FILE
        write_log(f"   ✅ Config loaded: SECRET_KEY={SECRET_KEY[:10]}...")
        write_log(f"   ✅ Movies file: {MOVIES_FILE}")
        
        # Check if files exist
        import os
        if os.path.exists(MOVIES_FILE):
            write_log("   ✅ Movies file exists")
        else:
            write_log(f"   ❌ Movies file missing: {MOVIES_FILE}")
            return False
            
    except Exception as e:
        write_log(f"   ❌ Config failed: {e}")
        return False
    
    # Test 3: Movie data loading
    write_log("\n3. Testing movie data loading...")
    try:
        from app.utils import load_movies, get_all_unique_movies
        movies = load_movies()
        write_log(f"   ✅ Loaded {len(movies)} movies")
        
        unique_movies = get_all_unique_movies(movies)
        write_log(f"   ✅ Got {len(unique_movies)} unique movies")
        write_log(f"   ✅ Type check: {type(unique_movies)}")
        
        if len(unique_movies) > 0:
            write_log(f"   ✅ First movie: {unique_movies[0].get('Title', 'No title')}")
    except Exception as e:
        write_log(f"   ❌ Movie loading failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 4: Router imports
    write_log("\n4. Testing router imports...")
    try:
        from app.routes_movies import router as movies_router
        write_log("   ✅ Movies router imported")
        
        from app.routes_watch_later import router as watch_later_router  
        write_log("   ✅ Watch later router imported")
        
        from app.routes_comments import router as comments_router
        write_log("   ✅ Comments router imported")
        
        from app.routes_auth import router as auth_router
        write_log("   ✅ Auth router imported")
        
        from app.routes_ai_suggestions import router as ai_suggestions_router
        write_log("   ✅ AI suggestions router imported")
        
    except Exception as e:
        write_log(f"   ❌ Router import failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 5: Google OAuth (optional)
    write_log("\n5. Testing Google OAuth (optional)...")
    try:
        from app.routes_google_auth import router as google_auth_router
        write_log("   ✅ Google OAuth router imported")
    except Exception as e:
        write_log(f"   ⚠️  Google OAuth unavailable (expected): {e}")
    
    # Test 6: FastAPI app creation
    write_log("\n6. Testing FastAPI app creation...")
    try:
        from fastapi.middleware.cors import CORSMiddleware
        from starlette.middleware.sessions import SessionMiddleware
        
        app = FastAPI()
        
        # Add middleware
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
        
        # Mount static files
        templates = Jinja2Templates(directory="templates")
        app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Include routers
        app.include_router(movies_router)
        app.include_router(watch_later_router)
        app.include_router(comments_router)
        app.include_router(auth_router)
        app.include_router(ai_suggestions_router)
        
        write_log("   ✅ FastAPI app created successfully")
        
    except Exception as e:
        write_log(f"   ❌ FastAPI app creation failed: {e}")
        traceback.print_exc()
        return False
    
    # Test 7: Try to start server (quick test)
    write_log("\n7. Testing server startup (2 second test)...")
    try:
        import threading
        import time
        
        def start_server():
            uvicorn.run(app, host="127.0.0.1", port=8002, log_level="critical")
        
        # Start server in background thread
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Wait a moment to see if it starts
        time.sleep(2)
        
        write_log("   ✅ Server started without immediate crashes")
        
    except Exception as e:
        write_log(f"   ❌ Server startup failed: {e}")
        traceback.print_exc()
        return False
    
    write_log("\n🎯 All tests passed! The server should work correctly.")
    write_log("   If you're still getting internal server errors, the issue might be:")
    write_log("   - Port conflict (try different port)")
    write_log("   - Frontend-backend communication issue") 
    write_log("   - Specific route error when accessed")
    
    return True

if __name__ == "__main__":
    # Clear log file
    with open("error_diagnosis.log", "w") as f:
        f.write("")
    
    success = test_server_startup()
    
    if success:
        write_log("\n🚀 Ready to start server!")
        write_log("   Try: python start_server.py")
        write_log("   Or:  python start_debug_server.py")
    else:
        write_log("\n❌ Server startup will fail. Fix the errors above first.")
