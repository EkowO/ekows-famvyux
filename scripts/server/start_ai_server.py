"""
Simple Server Starter
Start the MovieHub server with AI movie suggestions
"""

if __name__ == "__main__":
    import uvicorn
    print("🎬 Starting MovieHub with AI Movie Suggestions...")
    print("🤖 AI Assistant available at: http://localhost:8000/browse")
    print("📱 Features:")
    print("   • Browse movies with advanced filters")
    print("   • Chat with AI for personalized recommendations")
    print("   • Get explanations for why each movie fits your taste")
    print("=" * 50)
    
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
