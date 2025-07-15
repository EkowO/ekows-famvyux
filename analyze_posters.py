import json

# Load the movie database
with open('data/get movies/all_10000_movies.json', 'r') as f:
    movies = json.load(f)

# Check poster URL patterns
tmdb_posters = []
amazon_posters = []
no_posters = []

for movie in movies:
    poster = movie.get('Poster', '')
    if not poster or poster == 'N/A':
        no_posters.append(movie)
    elif poster.startswith('/'):
        tmdb_posters.append(movie)
    elif 'amazon' in poster:
        amazon_posters.append(movie)

print(f"Total movies: {len(movies)}")
print(f"Movies with TMDB poster paths (starting with /): {len(tmdb_posters)}")
print(f"Movies with Amazon poster URLs: {len(amazon_posters)}")
print(f"Movies with no posters: {len(no_posters)}")

print("\nSample TMDB poster paths:")
for movie in tmdb_posters[:5]:
    print(f"Title: {movie.get('Title')}, Poster: {movie.get('Poster')}")

print("\nSample Amazon poster URLs:")
for movie in amazon_posters[:3]:
    print(f"Title: {movie.get('Title')}, Poster: {movie.get('Poster')[:80]}...")
