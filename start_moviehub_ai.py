#!/usr/bin/env python3

"""
Start MovieHub Server with AI Bot
Starts the server and shows you how to access the AI movie recommendations.
"""

import subprocess
import sys
import time

def start_server():
    print("🎬 Starting MovieHub with AI Movie Recommendations")
    print("=" * 50)
    print("🤖 AI Bot Features:")
    print("   • Conversational movie recommendations")
    print("   • Smart preference detection") 
    print("   • Detailed explanations for each suggestion")
    print("   • Interactive chat interface")
    print()
    print("⚠️  Note: OAuth warning is normal and doesn't affect the AI bot")
    print("=" * 50)
    print()
    print("🌐 Server starting at: http://localhost:8000")
    print("🎯 AI Chat available at: http://localhost:8000/browse")
    print()
    print("💬 Try asking the AI:")
    print("   'I want funny action movies'")
    print("   'Suggest scary movies from the 80s'")
    print("   'What are good romantic comedies?'")
    print()
    print("🚀 Starting server...")
    print("=" * 50)
    
    # Start the server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "127.0.0.1", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using MovieHub AI!")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
        print("💡 Make sure you're in the correct directory and have all dependencies installed")

if __name__ == "__main__":
    start_server()
