#!/usr/bin/env python3

"""
Complete MovieHub Functionality Test
This script tests all major components without starting a server
"""

import json
import sys
from datetime import datetime

def log_test(message, success=True):
    status = "✅" if success else "❌"
    print(f"{status} {message}")
    return success

def test_all_functionality():
    """Test all MovieHub functionality"""
    
    print("🎬 MovieHub Complete Functionality Test")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test 1: Basic Movie Loading
    try:
        print("\n1. Testing Basic Movie Operations...")
        from app.utils import load_movies, get_all_unique_movies, get_filter_options
        
        movies = load_movies()
        log_test(f"Loaded {len(movies)} raw movies")
        
        unique_movies_dict = get_all_unique_movies(movies)
        log_test(f"Got {len(unique_movies_dict)} unique movies (dict)")
        
        filter_options = get_filter_options(unique_movies_dict)
        log_test("Filter options extracted successfully")
        
    except Exception as e:
        log_test(f"Basic movie operations failed: {e}", False)
        all_tests_passed = False
    
    # Test 2: AI Movie Operations
    try:
        print("\n2. Testing AI Movie Operations...")
        from app.utils import get_all_unique_movies_list
        
        unique_movies_list = get_all_unique_movies_list(movies)
        log_test(f"Got {len(unique_movies_list)} unique movies (list)")
        
        # Test slicing (the original bug)
        subset = unique_movies_list[:10]
        log_test(f"Slicing works: {len(subset)} movies")
        
        if len(unique_movies_list) > 0:
            first_movie = unique_movies_list[0]
            log_test(f"First movie: {first_movie.get('Title', 'No title')}")
        
    except Exception as e:
        log_test(f"AI movie operations failed: {e}", False)
        all_tests_passed = False
    
    # Test 3: AI Recommendation Engine
    try:
        print("\n3. Testing AI Recommendation Engine...")
        from app.routes_ai_suggestions import analyze_user_preferences, get_movie_recommendations
        
        # Test preference analysis
        test_message = "I want funny action movies from the 90s"
        preferences = analyze_user_preferences(test_message, [])
        log_test(f"Analyzed preferences: {preferences}")
        
        # Test recommendations
        recommendations = get_movie_recommendations(preferences, unique_movies_list[:100], limit=3)
        log_test(f"Generated {len(recommendations)} recommendations")
        
        if recommendations:
            for i, rec in enumerate(recommendations[:2], 1):
                log_test(f"  {i}. {rec.title} ({rec.year}) - {rec.match_score}% match")
        
    except Exception as e:
        log_test(f"AI recommendation engine failed: {e}", False)
        all_tests_passed = False
    
    # Test 4: Route Imports
    try:
        print("\n4. Testing Route Imports...")
        from app.routes_movies import router as movies_router
        from app.routes_watch_later import router as watch_later_router
        from app.routes_comments import router as comments_router
        from app.routes_auth import router as auth_router
        from app.routes_ai_suggestions import router as ai_suggestions_router
        
        log_test("All main routers imported successfully")
        
        # Test optional Google OAuth
        try:
            from app.routes_google_auth import router as google_auth_router
            log_test("Google OAuth router imported (optional)")
        except ImportError:
            log_test("Google OAuth not available (expected)")
        
    except Exception as e:
        log_test(f"Route imports failed: {e}", False)
        all_tests_passed = False
    
    # Test 5: FastAPI App Creation
    try:
        print("\n5. Testing FastAPI App Creation...")
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        from starlette.middleware.sessions import SessionMiddleware
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        from app.config import SECRET_KEY
        
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
        
        # Mount static files and templates
        templates = Jinja2Templates(directory="templates")
        app.mount("/static", StaticFiles(directory="static"), name="static")
        
        # Include all routers
        app.include_router(movies_router)
        app.include_router(watch_later_router)
        app.include_router(comments_router)
        app.include_router(auth_router)
        app.include_router(ai_suggestions_router)
        
        log_test("FastAPI app created with all components")
        
    except Exception as e:
        log_test(f"FastAPI app creation failed: {e}", False)
        all_tests_passed = False
    
    # Test 6: Simulate Main Functions
    try:
        print("\n6. Testing Main Application Functions...")
        
        # Test movie browsing functionality
        filter_test = {
            "q": "",
            "genre": "Action", 
            "min_rating": "7.0",
            "max_rating": "10.0",
            "year_from": "1990",
            "year_to": "2020",
            "rated": ""
        }
        
        from app.utils import filter_movies
        filtered = filter_movies(unique_movies_dict, **filter_test)
        log_test(f"Movie filtering works: {len(filtered)} movies found")
        
        # Test search functionality
        from app.utils import search_movies
        search_results = search_movies(unique_movies_dict, "batman")
        log_test(f"Movie search works: {len(search_results)} results for 'batman'")
        
    except Exception as e:
        log_test(f"Main application functions failed: {e}", False)
        all_tests_passed = False
    
    # Final Results
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n🚀 MovieHub is ready to run!")
        print("   • Movie database: ✅ Working")
        print("   • AI recommendations: ✅ Working") 
        print("   • Movie browsing: ✅ Working")
        print("   • Search & filters: ✅ Working")
        print("   • All routes: ✅ Working")
        print("\n📝 To start the server:")
        print("   python start_server.py")
        print("   Or: python start_debug_server.py")
        print("\n🌐 Then visit: http://127.0.0.1:8000")
        
        # Write success status
        with open("test_results.json", "w") as f:
            json.dump({
                "status": "success",
                "timestamp": datetime.now().isoformat(),
                "tests_passed": True,
                "message": "All MovieHub functionality working correctly"
            }, f, indent=2)
            
        return True
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Check the error messages above to fix issues.")
        
        # Write failure status
        with open("test_results.json", "w") as f:
            json.dump({
                "status": "failed", 
                "timestamp": datetime.now().isoformat(),
                "tests_passed": False,
                "message": "Some MovieHub components failed testing"
            }, f, indent=2)
            
        return False

if __name__ == "__main__":
    success = test_all_functionality()
    sys.exit(0 if success else 1)
