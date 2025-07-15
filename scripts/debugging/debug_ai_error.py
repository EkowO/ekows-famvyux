#!/usr/bin/env python3

"""
Debug AI Bot Error
Find out why the AI bot is failing
"""

import sys
import traceback
sys.path.append('.')

def debug_step_by_step():
    print("🔍 Debugging AI Bot Error Step by Step")
    print("=" * 50)
    
    # Step 1: Test imports
    print("1️⃣ Testing imports...")
    try:
        from app.routes_ai_suggestions import (
            analyze_user_preferences, 
            get_movie_recommendations,
            generate_ai_response,
            MovieSuggestionRequest,
            MovieRecommendation
        )
        print("✅ AI functions imported")
        
        from app.utils import load_movies, get_all_unique_movies
        print("✅ Utils imported")
        
        from fastapi.responses import JSONResponse
        from pydantic import BaseModel
        print("✅ FastAPI components imported")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 2: Test movie loading
    print("\n2️⃣ Testing movie loading...")
    try:
        movies = load_movies()
        print(f"✅ Raw movies loaded: {len(movies)}")
        
        all_movies = get_all_unique_movies(movies)
        print(f"✅ Unique movies: {len(all_movies)}")
        
        if all_movies:
            sample_movie = all_movies[0]
            print(f"✅ Sample movie: {sample_movie.get('Title', 'Unknown')}")
        else:
            print("⚠️ No movies found!")
            return False
            
    except Exception as e:
        print(f"❌ Movie loading failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 3: Test preference analysis
    print("\n3️⃣ Testing preference analysis...")
    try:
        test_message = "I want funny movies"
        preferences = analyze_user_preferences(test_message, [])
        print(f"✅ Preferences detected: {preferences}")
        
    except Exception as e:
        print(f"❌ Preference analysis failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 4: Test recommendations
    print("\n4️⃣ Testing recommendations...")
    try:
        # Use smaller dataset for testing
        test_movies = all_movies[:100] if len(all_movies) > 100 else all_movies
        recommendations = get_movie_recommendations(preferences, test_movies, limit=3)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"   {i}. {rec.title} ({rec.year}) - {rec.match_score}% match")
        
    except Exception as e:
        print(f"❌ Recommendation generation failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 5: Test AI response generation
    print("\n5️⃣ Testing AI response...")
    try:
        ai_response = generate_ai_response(test_message, recommendations, preferences)
        print(f"✅ AI response: {ai_response[:100]}...")
        
    except Exception as e:
        print(f"❌ AI response generation failed: {e}")
        traceback.print_exc()
        return False
    
    # Step 6: Test full API simulation
    print("\n6️⃣ Testing full API simulation...")
    try:
        # Simulate the API endpoint logic
        request_data = {
            "user_message": test_message,
            "conversation_history": []
        }
        
        # Load movies
        movies = load_movies()
        all_movies = get_all_unique_movies(movies)
        
        # Analyze preferences
        preferences = analyze_user_preferences(request_data["user_message"], request_data["conversation_history"])
        
        # Get recommendations
        recommendations = get_movie_recommendations(preferences, all_movies, limit=5)
        
        if not recommendations:
            response = {
                "ai_response": "I'm sorry, I couldn't find any movies matching your specific criteria.",
                "recommendations": [],
                "preferences_detected": preferences
            }
        else:
            ai_response = generate_ai_response(request_data["user_message"], recommendations, preferences)
            response = {
                "ai_response": ai_response,
                "recommendations": [rec.dict() for rec in recommendations],
                "preferences_detected": preferences
            }
        
        print(f"✅ Full API simulation successful")
        print(f"   Response contains {len(response['recommendations'])} recommendations")
        
    except Exception as e:
        print(f"❌ Full API simulation failed: {e}")
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("The AI bot should be working. The error might be elsewhere.")
    print("\nPossible issues:")
    print("• Server routing problem")
    print("• CORS issue")
    print("• JavaScript error in frontend")
    print("• Network connectivity")
    return True

def check_server_setup():
    print("\n" + "=" * 50)
    print("🌐 Checking Server Setup")
    print("=" * 50)
    
    try:
        import main
        print("✅ Main app can be imported")
        
        # Check if AI router is included
        app = main.app
        routes = [route.path for route in app.routes]
        
        if "/api/movie-suggestions" in routes:
            print("✅ AI API endpoint is registered")
        else:
            print("❌ AI API endpoint NOT found in routes")
            print("Available routes:", routes)
            
    except Exception as e:
        print(f"❌ Server setup check failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    success = debug_step_by_step()
    check_server_setup()
    
    if success:
        print("\n🎯 CONCLUSION:")
        print("The AI bot logic is working correctly.")
        print("The error is likely in the web interface or server communication.")
        print("\n🔧 To fix:")
        print("1. Check browser console for JavaScript errors")
        print("2. Verify the server is running on port 8000")
        print("3. Test the API endpoint directly")
    else:
        print("\n⚠️ Found issues in the AI bot logic that need fixing.")
