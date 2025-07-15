#!/usr/bin/env python3

"""
Test imports to find the source of the internal server error
"""

print("Testing imports...")

try:
    print("1. Testing FastAPI...")
    from fastapi import FastAPI
    print("   ✅ FastAPI imported successfully")
except Exception as e:
    print(f"   ❌ FastAPI import failed: {e}")

try:
    print("2. Testing app.config...")
    from app.config import SECRET_KEY
    print("   ✅ Config imported successfully")
except Exception as e:
    print(f"   ❌ Config import failed: {e}")

try:
    print("3. Testing movies router...")
    from app.routes_movies import router as movies_router
    print("   ✅ Movies router imported successfully")
except Exception as e:
    print(f"   ❌ Movies router import failed: {e}")

try:
    print("4. Testing AI router...")
    from app.routes_ai_suggestions import router as ai_suggestions_router
    print("   ✅ AI router imported successfully")
except Exception as e:
    print(f"   ❌ AI router import failed: {e}")

try:
    print("5. Testing all routers...")
    from app.routes_watch_later import router as watch_later_router
    from app.routes_comments import router as comments_router
    from app.routes_auth import router as auth_router
    print("   ✅ All other routers imported successfully")
except Exception as e:
    print(f"   ❌ Other routers import failed: {e}")

try:
    print("6. Testing Google OAuth (optional)...")
    from app.routes_google_auth import router as google_auth_router
    print("   ✅ Google OAuth router imported successfully")
except Exception as e:
    print(f"   ⚠️  Google OAuth import failed (expected): {e}")

try:
    print("7. Testing FastAPI app creation...")
    app = FastAPI()
    print("   ✅ FastAPI app created successfully")
except Exception as e:
    print(f"   ❌ FastAPI app creation failed: {e}")

print("\n🎯 Import test completed!")
