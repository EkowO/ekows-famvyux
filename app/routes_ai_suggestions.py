"""
AI Movie Recommendation Engine
This module provides AI-powered movie suggestions based on user preferences.
"""

import json
import random
from typing import List, Dict, Any
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Import movie utilities
from .utils import load_movies, get_all_unique_movies_list

router = APIRouter()

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
    match_score: int  # 1-100

def analyze_user_preferences(user_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Analyze user message to extract movie preferences"""
    message_lower = user_message.lower()
    
    # Genre preferences
    genre_keywords = {
        'action': ['action', 'fight', 'battle', 'war', 'martial arts', 'superhero', 'adventure'],
        'comedy': ['funny', 'comedy', 'laugh', 'humor', 'hilarious', 'amusing'],
        'drama': ['drama', 'emotional', 'serious', 'deep', 'character', 'touching'],
        'horror': ['scary', 'horror', 'frightening', 'terror', 'spooky', 'creepy'],
        'romance': ['romantic', 'love', 'romance', 'relationship', 'dating'],
        'sci-fi': ['sci-fi', 'science fiction', 'space', 'future', 'alien', 'robot'],
        'thriller': ['thriller', 'suspense', 'mystery', 'crime', 'detective'],
        'fantasy': ['fantasy', 'magic', 'wizard', 'dragon', 'supernatural'],
        'animation': ['animated', 'cartoon', 'animation', 'pixar', 'disney'],
        'documentary': ['documentary', 'real', 'true story', 'factual']
    }
    
    # Mood preferences
    mood_keywords = {
        'feel-good': ['feel good', 'uplifting', 'positive', 'happy', 'cheerful'],
        'dark': ['dark', 'gritty', 'noir', 'serious', 'intense'],
        'light': ['light', 'easy', 'casual', 'simple', 'relaxing'],
        'mind-bending': ['mind bending', 'complex', 'confusing', 'twist', 'puzzle']
    }
    
    # Era preferences
    era_keywords = {
        'classic': ['classic', 'old', 'vintage', 'golden age'],
        'modern': ['recent', 'new', 'latest', 'contemporary'],
        '80s': ['80s', 'eighties', '1980'],
        '90s': ['90s', 'nineties', '1990'],
        '2000s': ['2000s', 'early 2000'],
        '2010s': ['2010s', 'twenty tens']
    }
    
    # Rating preferences
    rating_keywords = {
        'family': ['family', 'kids', 'children', 'pg'],
        'mature': ['mature', 'adult', 'r rated', 'explicit']
    }
    
    preferences = {
        'genres': [],
        'moods': [],
        'eras': [],
        'ratings': [],
        'specific_requests': []
    }
    
    # Extract genre preferences
    for genre, keywords in genre_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            preferences['genres'].append(genre)
    
    # Extract mood preferences
    for mood, keywords in mood_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            preferences['moods'].append(mood)
    
    # Extract era preferences
    for era, keywords in era_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            preferences['eras'].append(era)
    
    # Extract rating preferences
    for rating, keywords in rating_keywords.items():
        if any(keyword in message_lower for keyword in keywords):
            preferences['ratings'].append(rating)
    
    # Specific movie requests
    specific_keywords = [
        'like', 'similar to', 'reminds me of', 'based on', 'directed by'
    ]
    
    for keyword in specific_keywords:
        if keyword in message_lower:
            preferences['specific_requests'].append(user_message)
            break
    
    return preferences

def calculate_movie_match_score(movie: Dict, preferences: Dict[str, Any]) -> tuple:
    """Calculate how well a movie matches user preferences"""
    score = 0
    reasons = []
    
    movie_genre = movie.get('Genre', '').lower()
    movie_year = int(movie.get('Year', '0')) if movie.get('Year', '0').isdigit() else 0
    movie_rating = movie.get('Rated', '').lower()
    movie_plot = movie.get('Plot', '').lower()
    
    # Genre matching (40 points max)
    genre_matches = 0
    for pref_genre in preferences.get('genres', []):
        if pref_genre in movie_genre:
            genre_matches += 1
            score += 20
            reasons.append(f"matches your {pref_genre} preference")
    
    # Mood matching (30 points max)
    for mood in preferences.get('moods', []):
        if mood == 'feel-good' and any(word in movie_plot for word in ['inspiring', 'uplifting', 'heartwarming']):
            score += 15
            reasons.append("has an uplifting story")
        elif mood == 'dark' and any(word in movie_plot for word in ['dark', 'crime', 'murder', 'death']):
            score += 15
            reasons.append("has a dark, intense atmosphere")
        elif mood == 'mind-bending' and any(word in movie_plot for word in ['twist', 'mystery', 'complex']):
            score += 15
            reasons.append("features complex storytelling")
    
    # Era matching (20 points max)
    for era in preferences.get('eras', []):
        if era == 'classic' and movie_year < 1980:
            score += 20
            reasons.append("is a classic film")
        elif era == '80s' and 1980 <= movie_year < 1990:
            score += 20
            reasons.append("is from the beloved 80s era")
        elif era == '90s' and 1990 <= movie_year < 2000:
            score += 20
            reasons.append("captures the 90s spirit")
        elif era == 'modern' and movie_year > 2010:
            score += 20
            reasons.append("is a modern film with contemporary themes")
    
    # Rating matching (10 points max)
    for rating_pref in preferences.get('ratings', []):
        if rating_pref == 'family' and movie_rating in ['g', 'pg', 'pg-13']:
            score += 10
            reasons.append("is family-friendly")
        elif rating_pref == 'mature' and movie_rating in ['r', 'nc-17']:
            score += 10
            reasons.append("has mature themes")
    
    # High IMDB rating bonus
    try:
        imdb_rating = float(movie.get('imdbRating', '0'))
        if imdb_rating >= 8.0:
            score += 10
            reasons.append(f"has an excellent IMDB rating of {imdb_rating}")
        elif imdb_rating >= 7.0:
            score += 5
            reasons.append(f"has a strong IMDB rating of {imdb_rating}")
    except (ValueError, TypeError):
        pass
    
    # Popular movie bonus (high vote count)
    try:
        vote_count_str = movie.get('imdbVotes', '0').replace(',', '')
        vote_count = int(vote_count_str)
        if vote_count > 100000:
            score += 5
            reasons.append("is widely acclaimed")
    except (ValueError, TypeError):
        pass
    
    return min(score, 100), "; ".join(reasons[:3])  # Cap at 100 and limit reasons

def get_movie_recommendations(preferences: Dict[str, Any], all_movies: List[Dict], limit: int = 5) -> List[MovieRecommendation]:
    """Get movie recommendations based on user preferences"""
    
    # Calculate match scores for all movies
    scored_movies = []
    for movie in all_movies:
        try:
            score, why = calculate_movie_match_score(movie, preferences)
            if score > 20:  # Only include movies with decent match
                scored_movies.append((movie, score, why))
        except (ValueError, KeyError, TypeError):
            continue  # Skip movies with invalid data
    
    # Sort by score
    scored_movies.sort(key=lambda x: x[1], reverse=True)
    
    # Get top recommendations
    recommendations = []
    for movie, score, why in scored_movies[:limit]:
        try:
            # Safely get movie data with defaults
            title = str(movie.get('Title', 'Unknown'))
            year = str(movie.get('Year', 'Unknown'))
            rating = str(movie.get('imdbRating', 'N/A'))
            genre = str(movie.get('Genre', 'Unknown'))
            plot = str(movie.get('Plot', 'No plot available'))
            poster = str(movie.get('Poster', '/static/no-image.png'))
            imdb_id = str(movie.get('imdbID', ''))
            
            # Ensure poster URL is valid
            if poster == 'N/A' or not poster or poster.strip() == '':
                poster = '/static/no-image.png'
            
            # Ensure why_recommended is a string
            why_recommended = str(why) if why else "matches your preferences"
            
            # Ensure match_score is an integer
            match_score = int(score) if isinstance(score, (int, float)) else 50
            
            rec = MovieRecommendation(
                title=title,
                year=year,
                rating=rating,
                genre=genre,
                plot=plot,
                poster=poster,
                imdb_id=imdb_id,
                why_recommended=why_recommended,
                match_score=match_score
            )
            recommendations.append(rec)
            
        except Exception as e:
            # Log the error but continue with other movies
            print(f"Error creating recommendation for {movie.get('Title', 'Unknown')}: {e}")
            continue
    
    # If we don't have enough high-scoring matches, add some popular movies
    if len(recommendations) < limit:
        try:
            popular_movies = []
            for m in all_movies:
                try:
                    rating_val = float(m.get('imdbRating', '0'))
                    if rating_val >= 7.5:
                        popular_movies.append(m)
                except (ValueError, TypeError):
                    continue
            
            popular_movies.sort(key=lambda x: float(x.get('imdbRating', '0')) if x.get('imdbRating', '0') != 'N/A' else 0, reverse=True)
            
            for movie in popular_movies:
                if len(recommendations) >= limit:
                    break
                
                # Check if already recommended
                movie_id = str(movie.get('imdbID', ''))
                if movie_id not in [r.imdb_id for r in recommendations]:
                    try:
                        rec = MovieRecommendation(
                            title=str(movie.get('Title', 'Unknown')),
                            year=str(movie.get('Year', 'Unknown')),
                            rating=str(movie.get('imdbRating', 'N/A')),
                            genre=str(movie.get('Genre', 'Unknown')),
                            plot=str(movie.get('Plot', 'No plot available')),
                            poster=str(movie.get('Poster', '/static/no-image.png')) if movie.get('Poster') != 'N/A' else '/static/no-image.png',
                            imdb_id=movie_id,
                            why_recommended="is highly rated and popular",
                            match_score=50
                        )
                        recommendations.append(rec)
                    except Exception as e:
                        print(f"Error creating popular movie recommendation: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error adding popular movies: {e}")
    
    return recommendations

def generate_ai_response(user_message: str, recommendations: List[MovieRecommendation], preferences: Dict[str, Any]) -> str:
    """Generate a conversational AI response with movie recommendations"""
    
    # Greeting responses
    greetings = [
        "I'd love to help you find the perfect movie! 🎬",
        "Great question! Let me suggest some movies you might enjoy. 🍿",
        "I've got some fantastic recommendations for you! ✨",
    ]
    
    # Analyze what the user asked for
    response_parts = [random.choice(greetings)]
    
    # Acknowledge their preferences
    if preferences.get('genres'):
        genres_str = ", ".join(preferences['genres'])
        response_parts.append(f"Based on your interest in {genres_str} movies, here are my top picks:")
    elif preferences.get('moods'):
        moods_str = ", ".join(preferences['moods'])
        response_parts.append(f"I understand you're looking for something {moods_str}. Here's what I recommend:")
    else:
        response_parts.append("Here are some excellent movies I think you'll enjoy:")
    
    return " ".join(response_parts)

@router.post("/api/movie-suggestions")
async def get_movie_suggestions(request: MovieSuggestionRequest):
    """API endpoint for getting AI movie suggestions"""
    print("🚀 AI API endpoint called")
    
    try:
        print(f"📝 User message: {request.user_message}")
        
        # Test 1: Load movies
        print("📚 Step 1: Loading movies...")
        try:
            movies = load_movies()
            print(f"✅ Raw movies loaded: {len(movies)}")
        except Exception as e:
            print(f"❌ Failed to load movies: {e}")
            return JSONResponse({
                "ai_response": f"Sorry, I couldn't access the movie database. Error: {str(e)}",
                "recommendations": [],
                "preferences_detected": {},
                "error": f"Movie loading failed: {str(e)}"
            })
        
        # Test 2: Get unique movies
        print("🎬 Step 2: Getting unique movies...")
        try:
            all_movies = get_all_unique_movies_list(movies)
            print(f"✅ Unique movies: {len(all_movies)}")
            print(f"✅ Movies type: {type(all_movies)}")
            
            if not all_movies:
                return JSONResponse({
                    "ai_response": "Sorry, no movies found in the database.",
                    "recommendations": [],
                    "preferences_detected": {},
                    "error": "No unique movies found"
                })
            
            # Ensure all_movies is a list
            if not isinstance(all_movies, list):
                all_movies = list(all_movies)
                print(f"🔄 Converted to list: {len(all_movies)} movies")
                
        except Exception as e:
            print(f"❌ Failed to get unique movies: {e}")
            import traceback
            traceback.print_exc()
            return JSONResponse({
                "ai_response": f"Sorry, I had trouble processing the movie database. Error: {str(e)}",
                "recommendations": [],
                "preferences_detected": {},
                "error": f"Unique movies failed: {str(e)}"
            })
        
        # Test 3: Analyze preferences
        print("🔍 Step 3: Analyzing preferences...")
        try:
            preferences = analyze_user_preferences(request.user_message, request.conversation_history)
            print(f"✅ Preferences detected: {preferences}")
        except Exception as e:
            print(f"❌ Failed to analyze preferences: {e}")
            return JSONResponse({
                "ai_response": f"Sorry, I couldn't understand your preferences. Error: {str(e)}",
                "recommendations": [],
                "preferences_detected": {},
                "error": f"Preference analysis failed: {str(e)}"
            })
        
        # Test 4: Get recommendations
        print("💡 Step 4: Getting recommendations...")
        try:
            # Use a smaller subset for testing to avoid memory issues
            if len(all_movies) > 1000:
                test_movies = all_movies[:1000]
                print(f"🔄 Using subset of {len(test_movies)} movies for faster processing")
            else:
                test_movies = all_movies
                print(f"🔄 Using all {len(test_movies)} movies")
                
            recommendations = get_movie_recommendations(preferences, test_movies, limit=5)
            print(f"✅ Generated {len(recommendations)} recommendations")
        except Exception as e:
            print(f"❌ Failed to get recommendations: {e}")
            return JSONResponse({
                "ai_response": f"Sorry, I couldn't generate movie recommendations. Error: {str(e)}",
                "recommendations": [],
                "preferences_detected": preferences,
                "error": f"Recommendation generation failed: {str(e)}"
            })
        
        # Test 5: Handle no recommendations
        if not recommendations:
            print("⚠️ No recommendations found")
            return JSONResponse({
                "ai_response": "I'm sorry, I couldn't find any movies matching your specific criteria. Could you try asking for a different genre or being more specific about what you're looking for?",
                "recommendations": [],
                "preferences_detected": preferences
            })
        
        # Test 6: Generate AI response
        print("🤖 Step 5: Generating AI response...")
        try:
            ai_response = generate_ai_response(request.user_message, recommendations, preferences)
            print(f"✅ AI response generated: {ai_response[:50]}...")
        except Exception as e:
            print(f"❌ Failed to generate AI response: {e}")
            ai_response = f"I found some great movies for you! Here are my recommendations:"
        
        # Test 7: Convert to dict format
        print("📄 Step 6: Converting to response format...")
        try:
            recommendations_dict = []
            for rec in recommendations:
                rec_dict = rec.dict()
                recommendations_dict.append(rec_dict)
            print(f"✅ Converted {len(recommendations_dict)} recommendations")
        except Exception as e:
            print(f"❌ Failed to convert recommendations: {e}")
            return JSONResponse({
                "ai_response": f"Sorry, I had trouble formatting the recommendations. Error: {str(e)}",
                "recommendations": [],
                "preferences_detected": preferences,
                "error": f"Format conversion failed: {str(e)}"
            })
        
        # Success!
        response_data = {
            "ai_response": ai_response,
            "recommendations": recommendations_dict,
            "preferences_detected": preferences
        }
        
        print(f"🎉 Success! Sending response with {len(recommendations_dict)} recommendations")
        return JSONResponse(response_data)
        
    except Exception as e:
        error_msg = f"Unexpected error in AI endpoint: {str(e)}"
        print(f"💥 {error_msg}")
        import traceback
        traceback.print_exc()
        
        return JSONResponse({
            "ai_response": "I'm experiencing some technical difficulties right now. Please try again in a moment, or try rephrasing your request.",
            "recommendations": [],
            "preferences_detected": {},
            "error": error_msg
        })
