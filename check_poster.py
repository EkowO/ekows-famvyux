import json

# Load the movie database
with open('data/get movies/all_10000_movies.json', 'r') as f:
    movies = json.load(f)

# Search for "9 days awake" movie
results = [m for m in movies if '9 days awake' in m.get('Title', '').lower()]

print(f"Found {len(results)} movies matching '9 days awake':")
for movie in results[:3]:
    print(f"Title: {movie.get('Title')}")
    print(f"Poster: {movie.get('Poster')}")
    print(f"Year: {movie.get('Year')}")
    print("---")

# Check a sample of other movies for poster URL patterns
print("\nSample of other movies and their poster URLs:")
for i, movie in enumerate(movies[:5]):
    print(f"Title: {movie.get('Title')}")
    print(f"Poster: {movie.get('Poster')}")
    print("---")
