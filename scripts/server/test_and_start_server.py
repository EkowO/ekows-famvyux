#!/usr/bin/env python3

"""
Direct server test - this will start the server and show any errors
"""

print("🚀 Testing server startup...")

try:
    # Import everything needed
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    from starlette.middleware.sessions import SessionMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates

    print("✅ FastAPI imports successful")

    # Import config
    from app.config import SECRET_KEY
    print("✅ Config imported")

    # Import all routers
    from app.routes_movies import router as movies_router
    from app.routes_watch_later import router as watch_later_router
    from app.routes_comments import router as comments_router
    from app.routes_auth import router as auth_router
    from app.routes_ai_suggestions import router as ai_suggestions_router
    
    print("✅ All routers imported")

    # Create app
    app = FastAPI()
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

    print("✅ Middleware added")

    # Setup templates and static files
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    print("✅ Templates and static files mounted")

    # Include routers
    app.include_router(movies_router)
    app.include_router(watch_later_router)
    app.include_router(comments_router)
    app.include_router(auth_router)
    app.include_router(ai_suggestions_router)
    
    print("✅ All routers included")

    # Try optional Google OAuth
    try:
        from app.routes_google_auth import router as google_auth_router
        app.include_router(google_auth_router)
        print("✅ Google OAuth authentication enabled")
    except ImportError as e:
        print(f"⚠️  Google OAuth authentication disabled: {e}")

    print("✅ App creation successful!")
    
    # Test AI functionality
    print("\n🤖 Testing AI functionality...")
    from app.utils import load_movies, get_all_unique_movies_list
    
    movies = load_movies()
    print(f"   📚 Loaded {len(movies)} movies")
    
    unique_movies = get_all_unique_movies_list(movies)
    print(f"   🎬 Got {len(unique_movies)} unique movies")
    print(f"   ✅ Type: {type(unique_movies)}")
    
    if len(unique_movies) > 0:
        # Test slicing (this was the bug)
        subset = unique_movies[:5]
        print(f"   ✅ Slicing works: {len(subset)} movies")
        print(f"   🎭 First movie: {unique_movies[0].get('Title', 'No title')}")
    
    print("✅ AI functionality test passed!")
    
    # Test regular movie functionality  
    print("\n🎬 Testing regular movie functionality...")
    from app.utils import get_all_unique_movies, get_filter_options
    
    regular_movies = get_all_unique_movies(movies)
    print(f"   📚 Got {len(regular_movies)} movies as dict")
    
    filter_options = get_filter_options(regular_movies)
    print(f"   🔧 Filter options extracted successfully")
    
    print("✅ Regular movie functionality test passed!")
    
    # Start server
    print("\n🚀 Starting server on port 8000...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    
    print(f"\n🔍 Error type: {type(e).__name__}")
    print(f"📝 Error details: {str(e)}")
    
    # Write error to file for inspection
    with open("startup_error.log", "w") as f:
        f.write(f"Startup Error: {e}\n")
        f.write(f"Error type: {type(e).__name__}\n")
        f.write("\nFull traceback:\n")
        traceback.print_exc(file=f)
