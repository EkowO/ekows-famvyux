#!/usr/bin/env python3
"""
Quick test script to start the server and open the browse page
"""
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    process = subprocess.Popen([
        "python", "-m", "uvicorn", "main:app", 
        "--reload", "--port", "8000", "--host", "0.0.0.0"
    ], cwd=Path(__file__).parent)
    
    # Wait a bit for server to start
    time.sleep(3)
    
    print("🌐 Opening browse page...")
    webbrowser.open("http://localhost:8000/browse")
    
    try:
        print("✅ Server running! Press Ctrl+C to stop")
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        process.terminate()

if __name__ == "__main__":
    start_server()
