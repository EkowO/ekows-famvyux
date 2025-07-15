#!/usr/bin/env python3
"""
Data Files Setup Script
Creates the necessary JSON data files for MovieHub application
"""

import json
import os
from pathlib import Path

def create_data_files():
    """Create necessary data files with default content"""
    
    # Get the data directory path
    data_dir = Path(__file__).parent.parent.parent / "data" / "get movies"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Define default content for each file
    files_to_create = {
        "movie_likes.json": {},
        "watch_later.json": {},
        "users.json": {},
        "comments.json": {},
    }
    
    # Check if all_10000_movies.json exists, if not, use sample
    movies_file = data_dir / "all_10000_movies.json"
    sample_file = data_dir / "movies_sample.json"
    
    if not movies_file.exists() and sample_file.exists():
        print("📋 Copying sample movies to main database...")
        try:
            with open(sample_file, 'r', encoding='utf-8') as f:
                sample_data = json.load(f)
            
            with open(movies_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2)
            
            print(f"✅ Created all_10000_movies.json with {len(sample_data)} sample movies")
        except Exception as e:
            print(f"❌ Error creating movies file: {e}")
    elif movies_file.exists():
        print("✅ all_10000_movies.json already exists")
    else:
        print("⚠️  No sample movies file found, creating empty movies database")
        files_to_create["all_10000_movies.json"] = []
    
    # Create other required files
    created_count = 0
    for filename, default_content in files_to_create.items():
        file_path = data_dir / filename
        
        if not file_path.exists():
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f, indent=2)
                print(f"✅ Created {filename}")
                created_count += 1
            except Exception as e:
                print(f"❌ Error creating {filename}: {e}")
        else:
            print(f"✅ {filename} already exists")
    
    print(f"\n📊 Setup Summary:")
    print(f"   Files created: {created_count}")
    print(f"   Data directory: {data_dir}")
    print("\n🚀 Your MovieHub application is ready to run!")
    print("   Run: python main.py")

if __name__ == "__main__":
    print("🎬 MovieHub Data Files Setup")
    print("=" * 40)
    create_data_files()
