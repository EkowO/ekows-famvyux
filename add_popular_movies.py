import json
import os
import requests
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
    existing_titles = set()
    for movie in movies:
        imdb_id = movie.get('imdbID')
        title = movie.get('Title', '').lower().strip()
        if imdb_id:
            existing_ids.add(imdb_id)
        if title:
            existing_titles.add(title)
    return existing_ids, existing_titles

def fetch_popular_movies_from_tmdb(api_key: str = None) -> List[Dict]:
    """Fetch popular movies from TMDB API (if API key is available)"""
    if not api_key:
        # Return some additional popular movies manually
        return [
            {
                "id": 299534,
                "title": "Avengers: Endgame",
                "release_date": "2019-04-26",
                "runtime": 181,
                "genres": "Action, Adventure, Drama",
                "overview": "After the devastating events of Avengers: Infinity War, the universe is in ruins due to the efforts of the Mad Titan, Thanos. With the help of remaining allies, the Avengers must assemble once more in order to undo Thanos' actions and restore order to the universe once and for all, no matter what consequences may be in store.",
                "original_language": "en",
                "production_countries": "United States",
                "poster_path": "/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
                "vote_average": 8.3,
                "vote_count": 23000,
                "imdb_id": "tt4154796",
                "revenue": 2797800564,
                "production_companies": "Marvel Studios, Walt Disney Pictures",
                "homepage": "https://www.marvel.com/movies/avengers-endgame"
            },
            {
                "id": 19995,
                "title": "Avatar",
                "release_date": "2009-12-18",
                "runtime": 162,
                "genres": "Action, Adventure, Fantasy, Science Fiction",
                "overview": "In the 22nd century, a paraplegic Marine is dispatched to the moon Pandora on a unique mission, but becomes torn between following orders and protecting an alien civilization.",
                "original_language": "en",
                "production_countries": "United States, United Kingdom",
                "poster_path": "/jRXYjXNq0Cs2TcJjLkki24MLp7u.jpg",
                "vote_average": 7.6,
                "vote_count": 29000,
                "imdb_id": "tt0499549",
                "revenue": 2923706026,
                "production_companies": "20th Century Fox, Lightstorm Entertainment",
                "homepage": "https://www.avatar.com/"
            },
            {
                "id": 11,
                "title": "Star Wars",
                "release_date": "1977-05-25",
                "runtime": 121,
                "genres": "Adventure, Action, Science Fiction",
                "overview": "Princess Leia is captured and held hostage by the evil Imperial forces in their effort to take over the galactic Empire. Venturesome Luke Skywalker and dashing captain Han Solo team together with the loveable robot duo R2-D2 and C-3PO to rescue the beautiful princess and restore peace and justice in the Empire.",
                "original_language": "en",
                "production_countries": "United States",
                "poster_path": "/6FfCtAuVAW8XJjZ7eWeLibRLWTw.jpg",
                "vote_average": 8.2,
                "vote_count": 20000,
                "imdb_id": "tt0076759",
                "revenue": 775398007,
                "production_companies": "Lucasfilm, 20th Century Fox",
                "homepage": "https://www.starwars.com/"
            },
            {
                "id": 550,
                "title": "Fight Club",
                "release_date": "1999-10-15",
                "runtime": 139,
                "genres": "Drama",
                "overview": "A ticking-time-bomb insomniac and a slippery soap salesman channel primal male aggression into a shocking new form of therapy. Their concept catches on, with underground \"fight clubs\" forming in every town, until an eccentric gets in the way and ignites an out-of-control spiral toward oblivion.",
                "original_language": "en",
                "production_countries": "United States",
                "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
                "vote_average": 8.4,
                "vote_count": 26000,
                "imdb_id": "tt0137523",
                "revenue": 100853753,
                "production_companies": "Fox 2000 Pictures, Regency Enterprises",
                "homepage": "N/A"
            },
            {
                "id": 122,
                "title": "The Lord of the Rings: The Return of the King",
                "release_date": "2003-12-17",
                "runtime": 201,
                "genres": "Adventure, Fantasy, Action",
                "overview": "Aragorn is revealed as the heir to the ancient kings as he, Gandalf and the other members of the broken fellowship struggle to save Gondor from Sauron's forces. Meanwhile, Frodo and Sam take the ring closer to the heart of Mordor, the dark lord's realm.",
                "original_language": "en",
                "production_countries": "New Zealand, United States",
                "poster_path": "/rCzpDGLbOoPwLjy3OAm5NUPOTrC.jpg",
                "vote_average": 8.7,
                "vote_count": 23000,
                "imdb_id": "tt0167260",
                "revenue": 1146030912,
                "production_companies": "New Line Cinema, WingNut Films",
                "homepage": "https://www.lordoftherings.net/"
            },
            {
                "id": 315162,
                "title": "Puss in Boots: The Last Wish",
                "release_date": "2022-12-21",
                "runtime": 103,
                "genres": "Animation, Adventure, Comedy, Family",
                "overview": "Puss in Boots discovers that his passion for adventure has come at a price: He has burned through eight of his nine lives, leaving him with only one life left. Puss sets out on an epic journey to find the mythical Last Wish and restore his nine lives.",
                "original_language": "en",
                "production_countries": "United States",
                "poster_path": "/kuf6dutpsT0vSVehic3EZIqkOBt.jpg",
                "vote_average": 8.2,
                "vote_count": 8500,
                "imdb_id": "tt3915174",
                "revenue": 484692560,
                "production_companies": "DreamWorks Animation",
                "homepage": "https://www.dreamworks.com/movies/puss-in-boots-the-last-wish"
            },
            {
                "id": 634649,
                "title": "Spider-Man: No Way Home",
                "release_date": "2021-12-17",
                "runtime": 148,
                "genres": "Action, Adventure, Science Fiction",
                "overview": "Peter Parker is unmasked and no longer able to separate his normal life from the high-stakes of being a super-hero. When he asks for help from Doctor Strange the stakes become even more dangerous, forcing him to discover what it truly means to be Spider-Man.",
                "original_language": "en",
                "production_countries": "United States",
                "poster_path": "/1g0dhYtq4irTY1GPXvft6k4YLjm.jpg",
                "vote_average": 8.1,
                "vote_count": 20000,
                "imdb_id": "tt10872600",
                "revenue": 1921847111,
                "production_companies": "Columbia Pictures, Marvel Studios, Pascal Pictures",
                "homepage": "https://www.spidermannowayhome.movie/"
            },
            {
                "id": 346698,
                "title": "Barbie",
                "release_date": "2023-07-21",
                "runtime": 114,
                "genres": "Comedy, Adventure",
                "overview": "Barbie and Ken are having the time of their lives in the colorful and seemingly perfect world of Barbie Land. However, when they get a chance to go to the real world, they soon discover the joys and perils of living among humans.",
                "original_language": "en",
                "production_countries": "United States, United Kingdom",
                "poster_path": "/iuFNMS8U5cb6xfzi51Dbkovj7vM.jpg",
                "vote_average": 7.1,
                "vote_count": 8000,
                "imdb_id": "tt1517268",
                "revenue": 1446113094,
                "production_companies": "Warner Bros. Pictures, Mattel Films, LuckyChap Entertainment",
                "homepage": "https://www.barbie-themovie.com/"
            }
        ]
    
    # If API key is provided, could fetch from TMDB API
    # This would require additional implementation
    return []

def convert_tmdb_to_omdb_format(tmdb_movie: Dict) -> Dict:
    """Convert TMDB format movie to OMDB format to match existing structure"""
    
    # Extract year from release_date
    release_date = tmdb_movie.get('release_date', '')
    year = release_date.split('-')[0] if release_date and release_date != '1500-01-01' else 'N/A'
    
    # Format runtime
    runtime = tmdb_movie.get('runtime', 0)
    runtime_str = f"{runtime} min" if runtime and runtime > 0 else "N/A"
    
    # Format revenue
    revenue = tmdb_movie.get('revenue', 0)
    box_office = f"${revenue:,}" if revenue > 0 else "N/A"
    
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
        "Poster": f"https://image.tmdb.org/t/p/w500{tmdb_movie.get('poster_path', '')}" if tmdb_movie.get('poster_path') else "N/A",
        "Ratings": [
            {
                "Source": "The Movie Database",
                "Value": f"{tmdb_movie.get('vote_average', 0)}/10"
            }
        ],
        "Metascore": "N/A",
        "imdbRating": str(tmdb_movie.get('vote_average', 'N/A')),
        "imdbVotes": f"{tmdb_movie.get('vote_count', 0):,}",
        "imdbID": tmdb_movie.get('imdb_id', f"tmdb{tmdb_movie.get('id', '')}"),
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": box_office,
        "Production": tmdb_movie.get('production_companies', 'N/A'),
        "Website": tmdb_movie.get('homepage', 'N/A'),
        "Response": "True"
    }
    
    return omdb_movie

def main():
    # Paths
    existing_movies_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\all_10000_movies.json"
    
    print("🎬 Loading existing movies...")
    existing_movies = load_existing_movies(existing_movies_file)
    print(f"📊 Found {len(existing_movies)} existing movies")
    
    # Get existing movie IDs and titles
    existing_ids, existing_titles = get_existing_movie_ids(existing_movies)
    print(f"🆔 Extracted {len(existing_ids)} unique movie IDs")
    print(f"📝 Extracted {len(existing_titles)} unique movie titles")
    
    # Get additional popular movies to add
    additional_movies = fetch_popular_movies_from_tmdb()
    
    # Check which movies are missing and convert them
    new_movies = []
    skipped_movies = []
    
    for tmdb_movie in additional_movies:
        imdb_id = tmdb_movie.get('imdb_id')
        title = tmdb_movie.get('title', '').lower().strip()
        
        # Check if movie already exists by IMDB ID or title
        if imdb_id in existing_ids:
            skipped_movies.append(f"{tmdb_movie['title']} (IMDB ID exists)")
        elif title in existing_titles:
            skipped_movies.append(f"{tmdb_movie['title']} (Title exists)")
        else:
            omdb_movie = convert_tmdb_to_omdb_format(tmdb_movie)
            new_movies.append(omdb_movie)
            print(f"✅ Will add: {omdb_movie['Title']} ({omdb_movie['Year']}) - Rating: {omdb_movie['imdbRating']}")
    
    # Show skipped movies
    if skipped_movies:
        print(f"\n⏭️ Skipped {len(skipped_movies)} existing movies:")
        for skipped in skipped_movies:
            print(f"   • {skipped}")
    
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
        print("✅ No new movies to add - all movies already exist!")
        
    print(f"\n📊 Final Statistics:")
    print(f"   🎬 Total movies in database: {len(existing_movies) + len(new_movies)}")
    print(f"   ➕ New movies added: {len(new_movies)}")
    print(f"   ⏭️ Movies skipped (already exist): {len(skipped_movies)}")

if __name__ == "__main__":
    main()
