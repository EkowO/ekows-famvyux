#!/usr/bin/env python3

"""
Manual AI API Test
Test the AI API endpoint manually to see the exact error
"""

import json
import sys
sys.path.append('.')

def test_ai_api_manually():
    print("🧪 Manual AI API Test")
    print("=" * 30)
    
    try:
        # Import the API function directly
        from app.routes_ai_suggestions import get_movie_suggestions, MovieSuggestionRequest
        
        # Create a test request
        test_request = MovieSuggestionRequest(
            user_message="I want funny movies",
            conversation_history=[]
        )
        
        print(f"📝 Test request: {test_request.user_message}")
        
        # Call the API function directly (without FastAPI)
        import asyncio
        
        async def run_test():
            try:
                response = await get_movie_suggestions(test_request)
                return response
            except Exception as e:
                print(f"❌ API call failed: {e}")
                import traceback
                traceback.print_exc()
                return None
        
        # Run the async function
        response = asyncio.run(run_test())
        
        if response:
            print("✅ API call successful!")
            # The response is a JSONResponse, get the body
            if hasattr(response, 'body'):
                body = json.loads(response.body.decode())
                print(f"📄 Response: {body.get('ai_response', 'No response')}")
                print(f"🎬 Recommendations: {len(body.get('recommendations', []))}")
            else:
                print(f"📄 Response type: {type(response)}")
        else:
            print("❌ API call failed")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_step_by_step_manual():
    print("\n" + "=" * 30)
    print("🔧 Step-by-Step Manual Test")
    print("=" * 30)
    
    try:
        # Step 1: Import functions
        from app.routes_ai_suggestions import (
            analyze_user_preferences,
            get_movie_recommendations, 
            generate_ai_response
        )
        from app.utils import load_movies, get_all_unique_movies
        print("✅ Step 1: Imports successful")
        
        # Step 2: Load movies
        movies = load_movies()
        all_movies = get_all_unique_movies(movies)
        print(f"✅ Step 2: Loaded {len(all_movies)} movies")
        
        # Step 3: Analyze preferences
        user_message = "I want funny movies"
        preferences = analyze_user_preferences(user_message, [])
        print(f"✅ Step 3: Preferences: {preferences}")
        
        # Step 4: Get recommendations
        recommendations = get_movie_recommendations(preferences, all_movies[:50], limit=3)
        print(f"✅ Step 4: Generated {len(recommendations)} recommendations")
        
        # Step 5: Generate response
        ai_response = generate_ai_response(user_message, recommendations, preferences)
        print(f"✅ Step 5: AI response: {ai_response[:50]}...")
        
        # Step 6: Convert to dict (like the API does)
        rec_dicts = [rec.dict() for rec in recommendations]
        print(f"✅ Step 6: Converted to {len(rec_dicts)} dictionaries")
        
        print("\n🎉 All steps successful!")
        
        if recommendations:
            print("\n🎬 Sample recommendations:")
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"   {i}. {rec.title} ({rec.year}) - {rec.match_score}% match")
                print(f"      Why: {rec.why_recommended}")
        
        return True
        
    except Exception as e:
        print(f"❌ Step failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_step_by_step_manual()
    
    if success:
        print("\n🎯 The AI logic works perfectly!")
        print("The error is likely in:")
        print("• FastAPI routing")
        print("• CORS configuration")
        print("• Frontend JavaScript")
        print("• Network communication")
        
        test_ai_api_manually()
    else:
        print("\n⚠️ Found issues in the AI logic.")
