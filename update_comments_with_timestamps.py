#!/usr/bin/env python3
"""
Script to update existing comments with timestamps
"""
import json
from datetime import datetime, timedelta
import random

def update_comments_with_timestamps():
    """Add timestamps to existing comments that don't have them"""
    
    # Load existing comments
    try:
        with open('get movies/comments.json', 'r') as f:
            comments = json.load(f)
    except FileNotFoundError:
        print("No comments file found")
        return
    
    # Current time
    now = datetime.now()
    
    # Update comments without timestamps
    updated_count = 0
    for movie_id, movie_comments in comments.items():
        for i, comment in enumerate(movie_comments):
            if 'timestamp' not in comment:
                # Add a random timestamp within the last 30 days
                days_ago = random.randint(0, 30)
                hours_ago = random.randint(0, 23)
                minutes_ago = random.randint(0, 59)
                
                comment_time = now - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
                comment['timestamp'] = comment_time.strftime("%Y-%m-%d %H:%M:%S")
                updated_count += 1
    
    # Save updated comments
    with open('get movies/comments.json', 'w') as f:
        json.dump(comments, f, indent=2)
    
    print(f"Updated {updated_count} comments with timestamps")

if __name__ == "__main__":
    update_comments_with_timestamps()
