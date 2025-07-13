#!/usr/bin/env python3

"""
Server startup script for MovieHub with Google OAuth
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Starting MovieHub server with Google OAuth...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("🔑 Google OAuth login: http://127.0.0.1:8000/login")
    print("📖 Setup guide: GOOGLE_OAUTH_SETUP.md")
    print("\n" + "="*50)
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
