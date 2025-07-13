import json
import os
from typing import List, Dict, Set

def load_existing_movies(file_path: str) -> List[Dict]:
    """Load existing movies from the JSON file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def get_existing_movie_ids(movies: List[Dict]) -> Set[str]:
    """Extract all existing movie IDs (imdbID) from the current dataset"""
    existing_ids = set()
    for movie in movies:
        imdb_id = movie.get('imdbID')
        if imdb_id:
            existing_ids.add(imdb_id)
    return existing_ids

def convert_tmdb_to_omdb_format(tmdb_movie: Dict) -> Dict:
    """Convert TMDB format movie to OMDB format to match existing structure"""
    
    # Extract year from release_date
    release_date = tmdb_movie.get('release_date', '')
    year = release_date.split('-')[0] if release_date and release_date != '1500-01-01' else 'N/A'
    
    # Format runtime
    runtime = tmdb_movie.get('runtime', 0)
    runtime_str = f"{runtime} min" if runtime and runtime > 0 else "N/A"
    
    # Create the movie in OMDB format
    omdb_movie = {
        "Title": tmdb_movie.get('title', 'N/A'),
        "Year": year,
        "Rated": "N/A",  # TMDB doesn't have direct equivalent
        "Released": tmdb_movie.get('release_date', 'N/A'),
        "Runtime": runtime_str,
        "Genre": tmdb_movie.get('genres', 'N/A'),
        "Director": "N/A",  # Would need additional API call
        "Writer": "N/A",   # Would need additional API call
        "Actors": "N/A",   # Would need additional API call
        "Plot": tmdb_movie.get('overview', 'N/A'),
        "Language": tmdb_movie.get('original_language', 'N/A'),
        "Country": tmdb_movie.get('production_countries', 'N/A'),
        "Awards": "N/A",   # TMDB doesn't have this field
        "Poster": f"https://image.tmdb.org/t/p/w300{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get('poster_path') else "N/A",
        "Ratings": [
            {
                "Source": "The Movie Database",
                "Value": f"{tmdb_movie.get('vote_average', 0)}/10"
            }
        ],
        "Metascore": "N/A",
        "imdbRating": str(tmdb_movie.get('vote_average', 'N/A')),
        "imdbVotes": str(tmdb_movie.get('vote_count', 0)).replace(',', ''),
        "imdbID": tmdb_movie.get('imdb_id', f"tmdb{tmdb_movie.get('id', '')}"),
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": f"${tmdb_movie.get('revenue', 0):,}" if tmdb_movie.get('revenue', 0) > 0 else "N/A",
        "Production": tmdb_movie.get('production_companies', 'N/A'),
        "Website": tmdb_movie.get('homepage', 'N/A'),
        "Response": "True"
    }
    
    return omdb_movie

def add_sample_popular_movies():
    """Add some popular movies that might be missing"""
    sample_movies = [
        {
            "id": 27205,
            "title": "Inception",
            "release_date": "2010-07-16",
            "runtime": 148,
            "genres": "Action, Science Fiction, Thriller",
            "overview": "Cobb, a skilled thief who commits corporate espionage by infiltrating the subconscious of his targets is offered a chance to regain his old life as payment for a task considered to be impossible: inception, the implantation of another person's idea into a target's subconscious.",
            "original_language": "en",
            "production_countries": "United States, United Kingdom",
            "poster_path": "/9gk7adHYeDvHkCSEqAvQNLV5Uge.jpg",
            "vote_average": 8.4,
            "vote_count": 35000,
            "imdb_id": "tt1375666",
            "revenue": 825532764,
            "production_companies": "Warner Bros. Pictures, Legendary Entertainment",
            "homepage": "https://www.warnerbros.com/movies/inception"
        },
        {
            "id": 155,
            "title": "The Dark Knight",
            "release_date": "2008-07-18",
            "runtime": 152,
            "genres": "Action, Crime, Drama",
            "overview": "Batman raises the stakes in his war on crime. With the help of Lt. Jim Gordon and District Attorney Harvey Dent, Batman sets out to dismantle the remaining criminal organizations that plague the streets. The partnership proves to be effective, but they soon find themselves prey to a reign of chaos unleashed by a rising criminal mastermind known to the terrified citizens of Gotham as the Joker.",
            "original_language": "en",
            "production_countries": "United States, United Kingdom",
            "poster_path": "/qJ2tW6WMUDux911r6m7haRef0WH.jpg",
            "vote_average": 9.0,
            "vote_count": 32000,
            "imdb_id": "tt0468569",
            "revenue": 1004558444,
            "production_companies": "Warner Bros. Pictures, Legendary Entertainment, Syncopy",
            "homepage": "https://www.warnerbros.com/movies/dark-knight"
        },
        {
            "id": 680,
            "title": "Pulp Fiction",
            "release_date": "1994-10-14",
            "runtime": 154,
            "genres": "Crime, Drama",
            "overview": "A burger-loving hit man, his philosophical partner, a drug-addled gangster's moll and a washed-up boxer converge in this sprawling, comedic crime caper. Their adventures unfurl in three stories that ingeniously trip back and forth in time.",
            "original_language": "en",
            "production_countries": "United States",
            "poster_path": "/d5iIlFn5s0ImszYzBPb8JPIfbXD.jpg",
            "vote_average": 8.9,
            "vote_count": 27000,
            "imdb_id": "tt0110912",
            "revenue": 214179088,
            "production_companies": "Miramax, A Band Apart",
            "homepage": "N/A"
        },
        {
            "id": 13,
            "title": "Forrest Gump",
            "release_date": "1994-07-06",
            "runtime": 142,
            "genres": "Comedy, Drama, Romance",
            "overview": "A man with a low IQ has accomplished great things in his life and been present during significant historic events—in each case, far exceeding what anyone imagined he could do. But despite all he has achieved, his one true love eludes him.",
            "original_language": "en",
            "production_countries": "United States",
            "poster_path": "/arw2vcBveWOVZr6pxd9XTd1TdQa.jpg",
            "vote_average": 8.5,
            "vote_count": 26000,
            "imdb_id": "tt0109830",
            "revenue": 677387716,
            "production_companies": "Paramount Pictures",
            "homepage": "N/A"
        },
        {
            "id": 496243,
            "title": "Parasite",
            "release_date": "2019-05-30",
            "runtime": 132,
            "genres": "Comedy, Thriller, Drama",
            "overview": "All unemployed, Ki-taek's family takes peculiar interest in the wealthy and glamorous Parks for their livelihood until they get entangled in an unexpected incident.",
            "original_language": "ko",
            "production_countries": "South Korea",
            "poster_path": "/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
            "vote_average": 8.5,
            "vote_count": 17000,
            "imdb_id": "tt6751668",
            "revenue": 258843537,
            "production_companies": "CJ Entertainment, Barunson E&A",
            "homepage": "N/A"
        }
    ]
    
    return sample_movies

def main():
    # Paths
    existing_movies_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\all_10000_movies.json"
    
    print("🎬 Loading existing movies...")
    existing_movies = load_existing_movies(existing_movies_file)
    print(f"📊 Found {len(existing_movies)} existing movies")
    
    # Get existing movie IDs
    existing_ids = get_existing_movie_ids(existing_movies)
    print(f"🆔 Extracted {len(existing_ids)} unique movie IDs")
    
    # Get sample movies to add
    sample_movies = add_sample_popular_movies()
    
    # Check which movies are missing and convert them
    new_movies = []
    for tmdb_movie in sample_movies:
        imdb_id = tmdb_movie.get('imdb_id')
        if imdb_id not in existing_ids:
            omdb_movie = convert_tmdb_to_omdb_format(tmdb_movie)
            new_movies.append(omdb_movie)
            print(f"✅ Will add: {omdb_movie['Title']} ({omdb_movie['Year']})")
        else:
            print(f"⏭️ Already exists: {tmdb_movie['title']}")
    
    if new_movies:
        print(f"\n🎬 Adding {len(new_movies)} new movies...")
        
        # Add new movies to existing list
        updated_movies = existing_movies + new_movies
        
        # Create backup
        backup_file = existing_movies_file.replace('.json', '_backup.json')
        print(f"💾 Creating backup: {backup_file}")
        
        try:
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(existing_movies, f, ensure_ascii=False, indent=2)
            print("✅ Backup created successfully")
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return
        
        # Save updated movies
        try:
            with open(existing_movies_file, 'w', encoding='utf-8') as f:
                json.dump(updated_movies, f, ensure_ascii=False, indent=2)
            print(f"✅ Successfully updated movie database!")
            print(f"📊 Total movies: {len(updated_movies)} (added {len(new_movies)})")
            
            # Show added movies
            print("\n🎬 Added movies:")
            for movie in new_movies:
                print(f"   • {movie['Title']} ({movie['Year']}) - IMDB: {movie['imdbRating']}")
                
        except Exception as e:
            print(f"❌ Error saving updated movies: {e}")
            print("🔄 Restoring from backup...")
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    backup_data = json.load(f)
                with open(existing_movies_file, 'w', encoding='utf-8') as f:
                    json.dump(backup_data, f, ensure_ascii=False, indent=2)
                print("✅ Restored from backup")
            except Exception as restore_error:
                print(f"❌ Error restoring backup: {restore_error}")
    else:
        print("✅ No new movies to add - all sample movies already exist!")

if __name__ == "__main__":
    main()
