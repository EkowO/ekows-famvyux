#!/usr/bin/env python3

"""
Minimal server test to check specific functionality
"""

print("🧪 Testing individual components...")

# Test 1: Basic imports
try:
    print("1. Testing basic imports...")
    from fastapi import FastAPI
    from app.config import SECRET_KEY
    print("   ✅ Basic imports work")
except Exception as e:
    print(f"   ❌ Basic imports failed: {e}")
    exit(1)

# Test 2: Movie utilities (old way)
try:
    print("2. Testing movie utilities (dict)...")
    from app.utils import load_movies, get_all_unique_movies, get_filter_options
    movies = load_movies()
    unique_dict = get_all_unique_movies(movies)
    print(f"   ✅ Dict version: {len(unique_dict)} movies")
    filter_opts = get_filter_options(unique_dict)
    print("   ✅ Filter options work")
except Exception as e:
    print(f"   ❌ Dict utilities failed: {e}")
    exit(1)

# Test 3: Movie utilities (new way)
try:
    print("3. Testing movie utilities (list)...")
    from app.utils import get_all_unique_movies_list
    unique_list = get_all_unique_movies_list(movies)
    print(f"   ✅ List version: {len(unique_list)} movies")
    subset = unique_list[:5]
    print(f"   ✅ Slicing works: {len(subset)} movies")
except Exception as e:
    print(f"   ❌ List utilities failed: {e}")
    exit(1)

# Test 4: All routers
try:
    print("4. Testing router imports...")
    from app.routes_movies import router as movies_router
    from app.routes_watch_later import router as watch_later_router
    from app.routes_comments import router as comments_router
    from app.routes_auth import router as auth_router
    from app.routes_ai_suggestions import router as ai_suggestions_router
    print("   ✅ All routers imported")
except Exception as e:
    print(f"   ❌ Router imports failed: {e}")
    exit(1)

# Test 5: Create minimal app
try:
    print("5. Creating minimal app...")
    app = FastAPI()
    app.include_router(movies_router)
    app.include_router(watch_later_router)
    app.include_router(comments_router)
    app.include_router(auth_router)
    app.include_router(ai_suggestions_router)
    print("   ✅ App created with all routers")
except Exception as e:
    print(f"   ❌ App creation failed: {e}")
    exit(1)

print("\n🎯 All tests passed! Starting minimal server on port 8003...")

try:
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="info")
except Exception as e:
    print(f"❌ Server start failed: {e}")
    with open("minimal_test_error.log", "w") as f:
        import traceback
        traceback.print_exc(file=f)
    print("   Error details written to minimal_test_error.log")
