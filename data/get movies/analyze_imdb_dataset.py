import pandas as pd
import re
import requests
import json
import time
from collections import Counter

# Load the IMDB dataset
print("Loading IMDB Dataset...")
df = pd.read_csv('IMDB Dataset.csv')
print(f"Total reviews: {len(df)}")

# Load existing movies
with open('all_10000_movies.json', 'r', encoding='utf-8') as f:
    existing_movies = json.load(f)

existing_titles = set(movie['Title'].lower() for movie in existing_movies)
print(f"Existing movies in JSON: {len(existing_movies)}")

# Common movie title patterns in reviews
def extract_movie_titles_from_reviews(reviews_sample):
    """Extract potential movie titles from reviews"""
    potential_titles = []
    
    # Sample reviews for analysis
    for review in reviews_sample:
        # Look for patterns like "Movie Name" or 'Movie Name'
        quoted_titles = re.findall(r'"([^"]+)"', review)
        single_quoted_titles = re.findall(r"'([^']+)'", review)
        
        potential_titles.extend(quoted_titles)
        potential_titles.extend(single_quoted_titles)
    
    return potential_titles

# Analyze a sample of reviews
print("\nAnalyzing sample reviews for movie titles...")
sample_reviews = df['review'].head(1000).tolist()
potential_titles = extract_movie_titles_from_reviews(sample_reviews)

# Filter out common non-movie phrases
common_words = ['the', 'and', 'or', 'but', 'if', 'then', 'so', 'this', 'that', 'these', 'those', 'a', 'an']
filtered_titles = [title for title in potential_titles if len(title) > 2 and title.lower() not in common_words]

# Count occurrences
title_counts = Counter(filtered_titles)
print(f"Found {len(filtered_titles)} potential movie titles")

# Show most common potential titles
if title_counts:
    print("\nMost common potential movie titles:")
    for title, count in title_counts.most_common(20):
        print(f"  {title}: {count} times")

# The IMDB Dataset.csv appears to be a sentiment analysis dataset with reviews
# It doesn't contain structured movie data like titles, years, etc.
# 
# Since the goal is to add all movies from IMDB to the JSON file,
# I'll suggest using the IMDB Top 1000 movies or similar dataset
# that actually contains movie titles and metadata

print("\n" + "="*50)
print("ANALYSIS RESULT:")
print("="*50)
print("The 'IMDB Dataset.csv' file contains movie reviews for sentiment analysis,")
print("not structured movie data with titles, years, directors, etc.")
print("\nTo add more movies to the JSON file, we would need:")
print("1. A dataset with actual movie titles and metadata")
print("2. Or use the OMDB API to fetch popular/top movies")
print("3. Or scrape IMDB for movie lists")
print("\nThe current approach of extracting titles from reviews is not reliable")
print("as reviews don't consistently mention movie titles in extractable format.")
