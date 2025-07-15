#!/usr/bin/env python3
"""
Simple route to test CSS and static file serving
"""
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/test-css", response_class=HTMLResponse)
async def test_css():
    """Test route to check CSS loading"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CSS Test</title>
        <link rel="stylesheet" href="/static/styles.css">
        <style>
            body { background: #000; color: #fff; padding: 20px; }
        </style>
    </head>
    <body>
        <h1>CSS Test Page</h1>
        <div class="ai-chat-container" style="display: block;">
            <div class="ai-chat-header">
                <h3>🎬 Test Header</h3>
            </div>
            <div class="ai-chat-messages">
                <div class="ai-message">
                    <div class="ai-avatar">🤖</div>
                    <div class="ai-text">Test message</div>
                </div>
            </div>
        </div>
        <script>
            console.log('CSS loaded:', !!document.styleSheets.length);
        </script>
    </body>
    </html>
    """

@app.get("/browse-test", response_class=HTMLResponse)
async def browse_test(request: Request):
    """Test the actual browse template"""
    return templates.TemplateResponse("browse_movies.html", {
        "request": request,
        "movies": [],
        "search_query": "",
        "current_page": 1,
        "total_pages": 1
    })

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting test server...")
    print("🌐 Test URLs:")
    print("   - CSS Test: http://localhost:8000/test-css")
    print("   - Browse Test: http://localhost:8000/browse-test")
    uvicorn.run(app, host="0.0.0.0", port=8000)
