#!/usr/bin/env python3

"""
Simple AI Error Finder
Find what's causing the AI bot technical difficulties
"""

import sys
import os

print("🔍 AI Bot Error Diagnosis")
print("=" * 40)

# Check 1: Python environment
print("1️⃣ Python Environment:")
print(f"   Python version: {sys.version}")
print(f"   Current directory: {os.getcwd()}")
print(f"   Python path: {sys.path[:3]}...")

# Check 2: File existence
print("\n2️⃣ File Existence:")
required_files = [
    "app/routes_ai_suggestions.py",
    "app/utils.py", 
    "get movies/all_10000_movies.json"
]

for file_path in required_files:
    if os.path.exists(file_path):
        print(f"   ✅ {file_path}")
    else:
        print(f"   ❌ {file_path} NOT FOUND")

# Check 3: Basic imports
print("\n3️⃣ Basic Imports:")
try:
    import json
    print("   ✅ json")
except Exception as e:
    print(f"   ❌ json: {e}")

try:
    from typing import List, Dict, Any
    print("   ✅ typing")
except Exception as e:
    print(f"   ❌ typing: {e}")

try:
    from fastapi import APIRouter
    print("   ✅ fastapi")
except Exception as e:
    print(f"   ❌ fastapi: {e}")

try:
    from pydantic import BaseModel
    print("   ✅ pydantic")
except Exception as e:
    print(f"   ❌ pydantic: {e}")

# Check 4: App imports
print("\n4️⃣ App Imports:")
sys.path.append('.')

try:
    from app.utils import load_movies
    print("   ✅ app.utils.load_movies")
except Exception as e:
    print(f"   ❌ app.utils.load_movies: {e}")

try:
    from app.routes_ai_suggestions import analyze_user_preferences
    print("   ✅ app.routes_ai_suggestions.analyze_user_preferences")
except Exception as e:
    print(f"   ❌ app.routes_ai_suggestions.analyze_user_preferences: {e}")

# Check 5: Movie data loading
print("\n5️⃣ Movie Data Loading:")
try:
    from app.utils import load_movies, get_all_unique_movies
    movies = load_movies()
    print(f"   ✅ Loaded {len(movies)} raw movies")
    
    unique_movies = get_all_unique_movies(movies)
    print(f"   ✅ Found {len(unique_movies)} unique movies")
    
    if unique_movies:
        sample = unique_movies[0]
        print(f"   ✅ Sample movie: {sample.get('Title', 'Unknown')}")
        print(f"   ✅ Has required fields: Title={sample.get('Title') is not None}, Year={sample.get('Year') is not None}")
    else:
        print("   ❌ No unique movies found")
        
except Exception as e:
    print(f"   ❌ Movie loading failed: {e}")
    import traceback
    traceback.print_exc()

# Check 6: AI function test
print("\n6️⃣ AI Function Test:")
try:
    from app.routes_ai_suggestions import analyze_user_preferences, get_movie_recommendations
    
    # Test preference analysis
    prefs = analyze_user_preferences("I want funny movies", [])
    print(f"   ✅ Preference analysis: {prefs}")
    
    # Test recommendations with small dataset
    if 'unique_movies' in locals():
        test_movies = unique_movies[:10] if len(unique_movies) > 10 else unique_movies
        recs = get_movie_recommendations(prefs, test_movies, limit=2)
        print(f"   ✅ Generated {len(recs)} recommendations")
        
        if recs:
            print(f"   ✅ Sample rec: {recs[0].title}")
    
except Exception as e:
    print(f"   ❌ AI function test failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
print("🎯 Diagnosis Complete")
print("Check the errors above to see what's failing.")

# Output to file for easier viewing
try:
    with open("ai_diagnosis.txt", "w") as f:
        f.write("AI Bot Diagnosis Results\n")
        f.write("=" * 30 + "\n")
        f.write("If you see this file, the script ran successfully.\n")
        f.write("Check the console output for detailed results.\n")
    print("\n📝 Results also saved to ai_diagnosis.txt")
except:
    pass
