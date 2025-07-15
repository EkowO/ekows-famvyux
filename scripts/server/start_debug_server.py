#!/usr/bin/env python3

"""
Start Server with AI Debug Logging
This will show detailed logs when the AI bot runs
"""

import uvicorn

if __name__ == "__main__":
    print("🚀 Starting MovieHub Server with AI Debug Logging")
    print("=" * 50)
    print("🤖 AI Bot will now show detailed error logs")
    print("🌐 Open: http://localhost:8000/browse")
    print("💬 Click 'Chat with AI' and try asking for movie recommendations")
    print("📺 Watch this terminal for detailed debug information")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1", 
        port=8000,
        reload=True,
        log_level="info"
    )
