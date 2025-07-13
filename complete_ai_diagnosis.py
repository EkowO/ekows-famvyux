#!/usr/bin/env python3

"""
Complete AI Bot Diagnostic
Find and fix the AI bot error
"""

import sys
import asyncio
import json
sys.path.append('.')

def run_complete_diagnosis():
    print("🔬 Complete AI Bot Diagnostic")
    print("=" * 50)
    
    # Test 1: Basic imports
    print("1️⃣ Testing basic imports...")
    try:
        from app.routes_ai_suggestions import (
            analyze_user_preferences,
            get_movie_recommendations,
            generate_ai_response,
            MovieSuggestionRequest,
            MovieRecommendation,
            get_movie_suggestions
        )
        from app.utils import load_movies, get_all_unique_movies
        print("✅ All imports successful")
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test 2: Data loading
    print("\n2️⃣ Testing data loading...")
    try:
        movies = load_movies()
        all_movies = get_all_unique_movies(movies)
        print(f"✅ Loaded {len(all_movies)} movies")
        
        if not all_movies:
            print("❌ No movies found!")
            return False
        
        # Check movie structure
        sample = all_movies[0]
        required_fields = ['Title', 'Year', 'Genre', 'imdbRating']
        missing_fields = [field for field in required_fields if field not in sample]
        
        if missing_fields:
            print(f"⚠️ Sample movie missing fields: {missing_fields}")
        else:
            print("✅ Movie data structure looks good")
            
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 3: Preference analysis
    print("\n3️⃣ Testing preference analysis...")
    try:
        test_messages = [
            "I want funny movies",
            "scary horror films",
            "action movies from the 90s"
        ]
        
        for msg in test_messages:
            prefs = analyze_user_preferences(msg, [])
            print(f"✅ '{msg}' → {prefs}")
            
    except Exception as e:
        print(f"❌ Preference analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 4: Movie recommendations
    print("\n4️⃣ Testing movie recommendations...")
    try:
        test_prefs = {'genres': ['comedy'], 'moods': [], 'eras': [], 'ratings': []}
        test_movies = all_movies[:100]  # Use subset for faster testing
        
        recommendations = get_movie_recommendations(test_prefs, test_movies, limit=3)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec.title} ({rec.year}) - {rec.match_score}%")
                
    except Exception as e:
        print(f"❌ Recommendation generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: API endpoint simulation
    print("\n5️⃣ Testing API endpoint simulation...")
    try:
        async def test_api():
            request = MovieSuggestionRequest(
                user_message="I want funny movies",
                conversation_history=[]
            )
            
            response = await get_movie_suggestions(request)
            return response
        
        # Run the async test
        response = asyncio.run(test_api())
        
        print(f"✅ API endpoint returned: {type(response)}")
        
        # Try to extract response data
        if hasattr(response, 'body'):
            try:
                body = json.loads(response.body.decode())
                print(f"✅ Response has {len(body.get('recommendations', []))} recommendations")
                print(f"✅ AI response: {body.get('ai_response', 'No response')[:50]}...")
            except Exception as e:
                print(f"⚠️ Could not parse response body: {e}")
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Check server registration
    print("\n6️⃣ Testing server registration...")
    try:
        import main
        app = main.app
        
        # Get all routes
        routes = []
        for route in app.routes:
            if hasattr(route, 'path'):
                routes.append(route.path)
        
        print(f"✅ App has {len(routes)} routes")
        
        if "/api/movie-suggestions" in routes:
            print("✅ AI API endpoint is registered")
        else:
            print("❌ AI API endpoint NOT found!")
            print("Available routes:", routes)
            return False
            
    except Exception as e:
        print(f"❌ Server registration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED!")
    print("The AI bot should be working correctly.")
    print("\nIf you're still getting errors, the issue is likely:")
    print("• Browser cache (try Ctrl+F5 to refresh)")
    print("• JavaScript console errors (check browser dev tools)")
    print("• Server not running on the correct port")
    print("• Network connectivity issues")
    
    return True

def show_browser_debug_steps():
    print("\n" + "=" * 50)
    print("🌐 BROWSER DEBUGGING STEPS")
    print("=" * 50)
    print("1. Start the server:")
    print("   python -m uvicorn main:app --reload --port 8000")
    print()
    print("2. Open browser to: http://localhost:8000/browse")
    print()
    print("3. Open Developer Tools (F12)")
    print()
    print("4. Click 'Chat with AI' button")
    print()
    print("5. Type a message and send")
    print()
    print("6. Check Console tab for JavaScript errors")
    print()
    print("7. Check Network tab to see if API request is sent")
    print()
    print("8. If you see 'fetch' request to /api/movie-suggestions:")
    print("   - Click on it to see the response")
    print("   - Check if it returns data or an error")
    print()
    print("9. Common issues:")
    print("   • CORS error → Server needs CORS middleware (fixed)")
    print("   • 404 error → API endpoint not registered (should be fixed)")
    print("   • 500 error → Server-side error (check server logs)")
    print("   • No request sent → JavaScript error (check console)")

if __name__ == "__main__":
    success = run_complete_diagnosis()
    
    if success:
        show_browser_debug_steps()
        print("\n✨ The AI bot logic is working perfectly!")
        print("Start the server and test in browser.")
    else:
        print("\n⚠️ Found issues that need to be fixed first.")
