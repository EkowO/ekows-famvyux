#!/usr/bin/env python3

"""
Minimal server test to identify internal server error
"""

import sys
import traceback

print("🚀 Starting minimal server test...")

try:
    print("1. Importing FastAPI...")
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    
    print("2. Creating app...")
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Server is working!"}
    
    @app.get("/test")
    async def test():
        return HTMLResponse("<h1>Test page working!</h1>")
    
    print("3. Testing our modules...")
    
    # Test config
    from app.config import SECRET_KEY
    print(f"   ✅ Config loaded, SECRET_KEY length: {len(SECRET_KEY)}")
    
    # Test utils
    from app.utils import load_movies, get_all_unique_movies
    movies = load_movies()
    unique_movies = get_all_unique_movies(movies)
    print(f"   ✅ Utils working: {len(unique_movies)} unique movies")
    
    # Test AI router
    from app.routes_ai_suggestions import router as ai_router
    print("   ✅ AI router imported successfully")
    
    app.include_router(ai_router)
    print("   ✅ AI router included successfully")
    
    print("4. Starting server...")
    import uvicorn
    
    print("🎯 If you see this, the error is likely in another router or middleware.")
    print("   Server should start at: http://127.0.0.1:8001")
    
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="debug")
    
except Exception as e:
    print(f"❌ Error found: {e}")
    print("\n📋 Full traceback:")
    traceback.print_exc()
    
    print(f"\n🔍 Error type: {type(e).__name__}")
    print(f"🔍 Error details: {str(e)}")
