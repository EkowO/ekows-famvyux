#!/usr/bin/env python3

"""
Final MovieHub Server - Comprehensive Startup
This script starts the MovieHub server with all fixes applied
"""

import sys
import uvicorn
from datetime import datetime

def main():
    print("🎬 MovieHub - Starting Server")
    print("=" * 40)
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Import and test all components first
        print("\n🔍 Pre-flight checks...")
        
        # Test basic imports
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from starlette.middleware.sessions import SessionMiddleware
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        print("   ✅ FastAPI components")
        
        # Test app configuration
        from app.config import SECRET_KEY
        print("   ✅ App configuration")
        
        # Test movie utilities
        from app.utils import (
            load_movies, 
            get_all_unique_movies,           # Returns dict (for compatibility)
            get_all_unique_movies_list,      # Returns list (for AI)
            get_filter_options
        )
        print("   ✅ Movie utilities")
        
        # Test data loading
        movies = load_movies()
        unique_dict = get_all_unique_movies(movies)
        unique_list = get_all_unique_movies_list(movies)
        print(f"   ✅ Movie data: {len(unique_dict)} movies (dict), {len(unique_list)} movies (list)")
        
        # Test all routers
        from app.routes_movies import router as movies_router
        from app.routes_watch_later import router as watch_later_router
        from app.routes_comments import router as comments_router
        from app.routes_auth import router as auth_router
        from app.routes_ai_suggestions import router as ai_suggestions_router
        print("   ✅ All routers")
        
        # Create the FastAPI application
        print("\n🛠️  Creating application...")
        app = FastAPI(
            title="MovieHub",
            description="AI-Powered Movie Recommendation Platform", 
            version="1.0.0"
        )
        
        # Add CORS middleware for cross-origin requests
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, specify your domain
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Add session middleware
        app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
        
        # Setup templates and static files
        templates = Jinja2Templates(directory="templates")
        app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Include all routers
        app.include_router(movies_router)
        app.include_router(watch_later_router)
        app.include_router(comments_router)
        app.include_router(auth_router)
        app.include_router(ai_suggestions_router)
        
        # Try to include Google OAuth (optional)
        try:
            from app.routes_google_auth import router as google_auth_router
            app.include_router(google_auth_router)
            print("   ✅ Google OAuth enabled")
        except ImportError as e:
            print(f"   ⚠️  Google OAuth disabled: {e}")
        
        print("   ✅ Application created successfully")
        
        # Test AI functionality specifically
        print("\n🤖 Testing AI functionality...")
        from app.routes_ai_suggestions import analyze_user_preferences
        test_prefs = analyze_user_preferences("I want action movies", [])
        print(f"   ✅ AI preference analysis: {test_prefs}")
        
        # Start the server
        print("\n🚀 Starting server...")
        print("   📍 URL: http://127.0.0.1:8000")
        print("   🏠 Home: http://127.0.0.1:8000/")
        print("   🔍 Browse: http://127.0.0.1:8000/browse")
        print("   🤖 AI Chat: Click 'Chat with AI' on browse page")
        print("   🔑 Login: http://127.0.0.1:8000/login")
        print("\n" + "=" * 40)
        print("📺 Server is running! Open your browser to test.")
        print("💬 Try the AI chatbot in the browse section!")
        print("🛑 Press Ctrl+C to stop the server")
        print("=" * 40)
        
        # Start the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=False,  # Disable reload for stability
            log_level="info",
            access_log=True
        )
        
    except Exception as e:
        print(f"\n❌ STARTUP FAILED: {e}")
        print("\n📋 Error Details:")
        import traceback
        traceback.print_exc()
        
        print(f"\n🔧 Common Solutions:")
        print("   1. Check if port 8000 is already in use")
        print("   2. Install missing packages: pip install -r requirements.txt")
        print("   3. Check file permissions")
        print("   4. Verify movie data files exist in 'get movies' folder")
        
        # Write error log
        with open("server_error.log", "w") as f:
            f.write(f"Server startup failed at {datetime.now()}\n")
            f.write(f"Error: {e}\n\n")
            traceback.print_exc(file=f)
        
        print(f"\n📝 Full error log written to: server_error.log")
        sys.exit(1)

if __name__ == "__main__":
    main()
