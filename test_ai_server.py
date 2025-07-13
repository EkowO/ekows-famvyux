#!/usr/bin/env python3

"""
Simple AI Test Server
Test the AI bot API directly
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Create a simple test app with just the AI functionality
app = FastAPI(title="AI Bot Test")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and add the AI router
try:
    from app.routes_ai_suggestions import router as ai_router
    app.include_router(ai_router)
    print("✅ AI router included successfully")
except Exception as e:
    print(f"❌ Failed to include AI router: {e}")
    import traceback
    traceback.print_exc()

@app.get("/")
async def root():
    return {"message": "AI Bot Test Server", "status": "running"}

@app.get("/test-ai")
async def test_ai():
    """Simple test endpoint"""
    try:
        from app.routes_ai_suggestions import analyze_user_preferences
        prefs = analyze_user_preferences("I want funny movies", [])
        return {"status": "AI working", "preferences": prefs}
    except Exception as e:
        return {"status": "AI error", "error": str(e)}

if __name__ == "__main__":
    print("🤖 Starting AI Bot Test Server")
    print("🌐 Access at: http://localhost:8001")
    print("🧪 Test endpoint: http://localhost:8001/test-ai")
    print("🎯 AI API: http://localhost:8001/api/movie-suggestions")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
        log_level="info"
    )
