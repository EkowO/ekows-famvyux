#!/usr/bin/env python3

"""
Simple Test Server for AI Bot
"""

import uvicorn
import sys
import os

if __name__ == "__main__":
    print("🤖 Starting MovieHub AI Bot Test Server...")
    print("🌐 Server will be available at: http://localhost:8000")
    print("🎬 Browse page with AI: http://localhost:8000/browse")
    print("=" * 50)
    
    try:
        # Import to test for errors
        import main
        print("✅ Main application imported successfully")
        
        # Start server
        uvicorn.run(
            "main:app", 
            host="127.0.0.1", 
            port=8000, 
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        import traceback
        traceback.print_exc()
