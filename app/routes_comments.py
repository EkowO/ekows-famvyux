from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from .utils import load_comments, save_comments
from datetime import datetime

router = APIRouter()

@router.post("/movie/{movie_id}/comment")
async def add_comment(request: Request, movie_id: str, comment: str = Form(...)):
    comments = load_comments()
    username = request.session.get("username")
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    movie_comments = comments.get(movie_id, [])
    
    # Add timestamp to the comment
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    movie_comments.append({
        "user": username, 
        "comment": comment,
        "timestamp": timestamp
    })
    
    comments[movie_id] = movie_comments
    save_comments(comments)
    return RedirectResponse(url=f"/movie/{movie_id}", status_code=303)