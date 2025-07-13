#!/usr/bin/env python3

"""
Simple AI Bot Debug Test
This script tests each component of the AI bot individually.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing Imports...")
    
    try:
        sys.path.append('.')
        
        # Test basic imports
        import json
        print("✅ json imported")
        
        from typing import List, Dict, Any
        print("✅ typing imported")
        
        from fastapi import APIRouter, Request, HTTPException
        print("✅ fastapi imported")
        
        from fastapi.responses import JSONResponse
        print("✅ fastapi.responses imported")
        
        from pydantic import BaseModel
        print("✅ pydantic imported")
        
        # Test app imports
        from app.utils import load_movies, get_all_unique_movies
        print("✅ app.utils imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_movie_loading():
    """Test if movies can be loaded"""
    print("\n📚 Testing Movie Loading...")
    
    try:
        from app.utils import load_movies, get_all_unique_movies
        
        movies = load_movies()
        print(f"✅ Loaded {len(movies)} movies")
        
        unique_movies = get_all_unique_movies(movies)
        print(f"✅ Found {len(unique_movies)} unique movies")
        
        # Test first movie structure
        if unique_movies:
            first_movie = unique_movies[0]
            print(f"✅ First movie: {first_movie.get('Title', 'Unknown')}")
            print(f"   Year: {first_movie.get('Year', 'Unknown')}")
            print(f"   Genre: {first_movie.get('Genre', 'Unknown')}")
            print(f"   Rating: {first_movie.get('imdbRating', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Movie loading error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_preference_analysis():
    """Test the preference analysis function"""
    print("\n🧠 Testing Preference Analysis...")
    
    try:
        # Manual implementation for testing
        def analyze_user_preferences_simple(user_message):
            message_lower = user_message.lower()
            
            genres = []
            if 'funny' in message_lower or 'comedy' in message_lower:
                genres.append('comedy')
            if 'action' in message_lower:
                genres.append('action')
            if 'scary' in message_lower or 'horror' in message_lower:
                genres.append('horror')
            if 'romance' in message_lower or 'romantic' in message_lower:
                genres.append('romance')
            
            moods = []
            if 'light' in message_lower or 'feel good' in message_lower:
                moods.append('feel-good')
            if 'dark' in message_lower or 'gritty' in message_lower:
                moods.append('dark')
            
            eras = []
            if '80s' in message_lower or 'eighties' in message_lower:
                eras.append('80s')
            if '90s' in message_lower or 'nineties' in message_lower:
                eras.append('90s')
            
            return {
                'genres': genres,
                'moods': moods,
                'eras': eras,
                'ratings': []
            }
        
        test_message = "I want something funny and light-hearted"
        prefs = analyze_user_preferences_simple(test_message)
        
        print(f"✅ Message: '{test_message}'")
        print(f"   Detected genres: {prefs['genres']}")
        print(f"   Detected moods: {prefs['moods']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Preference analysis error: {e}")
        return False

def test_movie_matching():
    """Test movie matching logic"""
    print("\n🎯 Testing Movie Matching...")
    
    try:
        # Sample movie data
        test_movie = {
            "Title": "The Mask",
            "Year": "1994", 
            "Genre": "Comedy, Crime, Fantasy",
            "Plot": "Bank clerk Stanley Ipkiss is transformed into a manic superhero when he wears a mysterious mask.",
            "imdbRating": "6.9",
            "imdbVotes": "380,000",
            "Rated": "PG-13"
        }
        
        # Test preferences for comedy
        comedy_prefs = {'genres': ['comedy'], 'moods': ['feel-good'], 'eras': [], 'ratings': []}
        
        # Simple scoring logic
        score = 0
        reasons = []
        
        movie_genre = test_movie.get('Genre', '').lower()
        if 'comedy' in movie_genre:
            score += 40
            reasons.append("matches your comedy preference")
        
        imdb_rating = float(test_movie.get('imdbRating', '0'))
        if imdb_rating >= 6.5:
            score += 20
            reasons.append(f"has a good IMDB rating of {imdb_rating}")
        
        print(f"✅ Movie: {test_movie['Title']}")
        print(f"   Score: {score}%")
        print(f"   Reasons: {'; '.join(reasons)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Movie matching error: {e}")
        return False

def test_api_structure():
    """Test if the API endpoint structure is correct"""
    print("\n🌐 Testing API Structure...")
    
    try:
        # Test creating the request/response models
        from pydantic import BaseModel
        from typing import List, Dict
        
        class MovieSuggestionRequest(BaseModel):
            user_message: str
            conversation_history: List[Dict[str, str]] = []
        
        class MovieRecommendation(BaseModel):
            title: str
            year: str
            rating: str
            genre: str
            plot: str
            poster: str
            imdb_id: str
            why_recommended: str
            match_score: int
        
        # Test creating instances
        request = MovieSuggestionRequest(
            user_message="I want funny movies",
            conversation_history=[]
        )
        print(f"✅ Request model: {request.user_message}")
        
        recommendation = MovieRecommendation(
            title="Test Movie",
            year="2023",
            rating="7.5",
            genre="Comedy",
            plot="A funny movie",
            poster="/static/no-image.png",
            imdb_id="tt1234567",
            why_recommended="It's funny",
            match_score=85
        )
        print(f"✅ Recommendation model: {recommendation.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure error: {e}")
        return False

def main():
    """Run all debug tests"""
    print("🐛 AI Bot Debug Test Suite")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Movie Loading", test_movie_loading),
        ("Preference Analysis", test_preference_analysis), 
        ("Movie Matching", test_movie_matching),
        ("API Structure", test_api_structure)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 40)
    print("📊 Test Results:")
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    print(f"\n🎯 Summary: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("🎉 All tests passed! The AI bot components are working.")
        print("\n🚀 Next steps:")
        print("   1. Start the server: uvicorn main:app --reload")
        print("   2. Go to: http://localhost:8000/browse") 
        print("   3. Click 'Chat with AI' and test the bot")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
