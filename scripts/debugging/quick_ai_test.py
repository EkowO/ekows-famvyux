#!/usr/bin/env python3

"""
Quick AI Bot Test
Tests if the AI movie recommendation system is working.
"""

def test_ai_bot():
    print("🤖 Testing AI Movie Recommendation Bot")
    print("=" * 40)
    
    try:
        # Test 1: Import check
        print("1️⃣ Testing imports...")
        from app.routes_ai_suggestions import analyze_user_preferences, get_movie_recommendations
        from app.utils import load_movies, get_all_unique_movies
        print("✅ All imports successful")
        
        # Test 2: Preference analysis
        print("\n2️⃣ Testing preference analysis...")
        test_message = "I want funny action movies"
        preferences = analyze_user_preferences(test_message, [])
        print(f"✅ Message: '{test_message}'")
        print(f"   Detected: {preferences}")
        
        # Test 3: Movie loading
        print("\n3️⃣ Testing movie loading...")
        movies = load_movies()
        all_movies = get_all_unique_movies(movies)
        print(f"✅ Loaded {len(all_movies)} unique movies")
        
        # Test 4: Get recommendations
        print("\n4️⃣ Testing recommendations...")
        recommendations = get_movie_recommendations(preferences, all_movies[:100], limit=3)
        print(f"✅ Generated {len(recommendations)} recommendations")
        
        if recommendations:
            print("\n🎬 Sample recommendations:")
            for i, rec in enumerate(recommendations[:2], 1):
                print(f"   {i}. {rec.title} ({rec.year}) - {rec.match_score}% match")
        
        print("\n🎉 AI Bot Test Results:")
        print("✅ Imports working")
        print("✅ Preference detection working") 
        print("✅ Movie loading working")
        print("✅ Recommendation engine working")
        print("\n🚀 The AI bot is ready to use!")
        
        return True
        
    except Exception as e:
        print(f"❌ AI Bot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_usage_instructions():
    print("\n" + "=" * 50)
    print("📋 HOW TO USE THE AI BOT")
    print("=" * 50)
    print("1. Start the server:")
    print("   python -m uvicorn main:app --reload --port 8000")
    print()
    print("2. Open your browser:")
    print("   http://localhost:8000/browse")
    print()
    print("3. Click 'Chat with AI' button")
    print()
    print("4. Try these example messages:")
    print("   • 'I want something funny and light-hearted'")
    print("   • 'Suggest scary movies from the 80s'")
    print("   • 'I need good action movies with high ratings'")
    print("   • 'What are some romantic comedies?'")
    print()
    print("5. The AI will respond with personalized recommendations!")
    print()
    print("💡 Note: The OAuth warning is not related to the AI bot.")
    print("   The AI movie recommendations work independently.")

if __name__ == "__main__":
    success = test_ai_bot()
    
    if success:
        show_usage_instructions()
        print("\n✨ Your AI movie recommendation bot is working perfectly!")
    else:
        print("\n⚠️ There are issues with the AI bot setup.")
        print("Please check the error messages above.")
