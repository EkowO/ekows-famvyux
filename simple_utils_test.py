#!/usr/bin/env python3

"""
Simple test to check if the utils.py fix works
"""

import sys
import json

# Add current directory to path
sys.path.append('.')

print("🧪 Testing utils.py fix...")

try:
    print("1. Importing utils...")
    from app.utils import load_movies, get_all_unique_movies
    print("   ✅ Utils imported successfully")
    
    print("2. Loading movies...")
    movies = load_movies()
    print(f"   ✅ Loaded {len(movies)} movies")
    
    print("3. Getting unique movies...")
    unique_movies = get_all_unique_movies(movies)
    print(f"   ✅ Got {len(unique_movies)} unique movies")
    print(f"   ✅ Type: {type(unique_movies)}")
    
    if isinstance(unique_movies, list) and len(unique_movies) > 0:
        print(f"   ✅ First movie: {unique_movies[0].get('Title', 'No title')}")
        
        # Test slicing
        print("4. Testing slicing...")
        subset = unique_movies[:5]
        print(f"   ✅ Sliced to {len(subset)} movies")
        
        print("✅ All tests passed! The utils.py fix works correctly.")
    else:
        print("❌ unique_movies is not a proper list")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
