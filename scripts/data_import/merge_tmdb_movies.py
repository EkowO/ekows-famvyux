#!/usr/bin/env python3
"""
TMDB Movie Dataset Integration Script
Adds unique movies from TMDB dataset to the existing all_10000_movies.json
Avoids duplicates by checking title and year matches
"""

import json
import csv
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple

# File paths
BASE_DIR = Path(__file__).parent / "data" / "get movies"
EXISTING_MOVIES_FILE = BASE_DIR / "all_10000_movies.json"
TMDB_CSV_FILE = BASE_DIR / "TMDB_movie_dataset_v11.csv"
BACKUP_FILE = BASE_DIR / "all_10000_movies_backup.json"
OUTPUT_FILE = BASE_DIR / "all_10000_movies.json"

class MovieMerger:
    def __init__(self):
        self.existing_movies = []
        self.tmdb_movies = []
        self.duplicates_found = 0
        self.movies_added = 0
        
    def normalize_title(self, title: str) -> str:
        """Normalize title for comparison"""
        if not title:
            return ""
        
        # Remove articles, special characters, convert to lowercase
        title = title.lower().strip()
        title = re.sub(r'^(the|a|an)\s+', '', title)
        title = re.sub(r'[^\w\s]', '', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title
    
    def extract_year(self, date_str: str) -> str:
        """Extract year from various date formats"""
        if not date_str:
            return ""
        
        # Try to extract 4-digit year
        year_match = re.search(r'\b(19|20)\d{2}\b', str(date_str))
        return year_match.group(0) if year_match else ""
    
    def load_existing_movies(self):
        """Load existing movies from JSON file"""
        print("📁 Loading existing movies...")
        
        if not EXISTING_MOVIES_FILE.exists():
            print("❌ Existing movies file not found!")
            return False
        
        try:
            with open(EXISTING_MOVIES_FILE, 'r', encoding='utf-8') as f:
                self.existing_movies = json.load(f)
            
            print(f"✅ Loaded {len(self.existing_movies)} existing movies")
            return True
        except Exception as e:
            print(f"❌ Error loading existing movies: {e}")
            return False
    
    def load_tmdb_movies(self):
        """Load and parse TMDB CSV dataset"""
        print("📁 Loading TMDB dataset...")
        
        if not TMDB_CSV_FILE.exists():
            print("❌ TMDB dataset file not found!")
            return False
        
        try:
            with open(TMDB_CSV_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    movie = self.convert_tmdb_to_movie_format(row)
                    if movie:
                        self.tmdb_movies.append(movie)
            
            print(f"✅ Loaded {len(self.tmdb_movies)} TMDB movies")
            return True
        except Exception as e:
            print(f"❌ Error loading TMDB dataset: {e}")
            return False
    
    def convert_tmdb_to_movie_format(self, tmdb_row: Dict) -> Dict:
        """Convert TMDB CSV row to our movie format"""
        try:
            # Skip adult movies
            if tmdb_row.get('adult', '').lower() == 'true':
                return None
            
            # Extract year from release_date
            release_year = self.extract_year(tmdb_row.get('release_date', ''))
            
            # Convert runtime to "X min" format
            runtime = tmdb_row.get('runtime', '')
            if runtime and runtime.isdigit():
                runtime = f"{runtime} min"
            else:
                runtime = "N/A"
            
            # Process genres
            genres = tmdb_row.get('genres', '')
            if genres:
                # Clean up genres string
                genres = genres.replace('[', '').replace(']', '').replace("'", "")
            else:
                genres = "N/A"
            
            # Build poster URL
            poster_path = tmdb_row.get('poster_path', '')
            poster_url = ""
            if poster_path and poster_path != 'null':
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            
            # Create movie object in our format
            movie = {
                "Title": tmdb_row.get('title', tmdb_row.get('original_title', '')),
                "Year": release_year,
                "Rated": "N/A",  # TMDB doesn't have ratings like MPAA
                "Released": tmdb_row.get('release_date', ''),
                "Runtime": runtime,
                "Genre": genres,
                "Director": "N/A",  # Not available in this TMDB dataset
                "Writer": "N/A",   # Not available in this TMDB dataset
                "Actors": "N/A",   # Not available in this TMDB dataset
                "Plot": tmdb_row.get('overview', ''),
                "Language": self.format_language(tmdb_row.get('original_language', '')),
                "Country": self.format_countries(tmdb_row.get('production_countries', '')),
                "Awards": "N/A",
                "Poster": poster_url,
                "Ratings": [
                    {
                        "Source": "The Movie Database",
                        "Value": f"{tmdb_row.get('vote_average', '0')}/10"
                    }
                ],
                "Metascore": "N/A",
                "imdbRating": tmdb_row.get('vote_average', '0'),
                "imdbVotes": tmdb_row.get('vote_count', '0'),
                "imdbID": tmdb_row.get('imdb_id', ''),
                "Type": "movie",
                "DVD": "N/A",
                "BoxOffice": self.format_revenue(tmdb_row.get('revenue', '')),
                "Production": self.format_production_companies(tmdb_row.get('production_companies', '')),
                "Website": tmdb_row.get('homepage', ''),
                "Response": "True",
                "tmdb_id": tmdb_row.get('id', ''),
                "tmdb_popularity": tmdb_row.get('popularity', ''),
                "tmdb_tagline": tmdb_row.get('tagline', '')
            }
            
            return movie
            
        except Exception as e:
            print(f"⚠️ Error converting TMDB row: {e}")
            return None
    
    def format_language(self, lang_code: str) -> str:
        """Convert language code to full name"""
        lang_map = {
            'en': 'English', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
            'it': 'Italian', 'ja': 'Japanese', 'ko': 'Korean', 'zh': 'Chinese',
            'ru': 'Russian', 'pt': 'Portuguese', 'hi': 'Hindi', 'ar': 'Arabic'
        }
        return lang_map.get(lang_code, lang_code.upper() if lang_code else 'English')
    
    def format_countries(self, countries_str: str) -> str:
        """Format production countries"""
        if not countries_str or countries_str == 'null':
            return "N/A"
        # Remove extra formatting and return first country
        countries = countries_str.replace('[', '').replace(']', '').replace("'", "")
        return countries.split(',')[0].strip() if countries else "N/A"
    
    def format_revenue(self, revenue: str) -> str:
        """Format revenue as currency"""
        if not revenue or revenue == '0' or revenue == 'null':
            return "N/A"
        try:
            amount = int(float(revenue))
            return f"${amount:,}"
        except:
            return "N/A"
    
    def format_production_companies(self, companies_str: str) -> str:
        """Format production companies"""
        if not companies_str or companies_str == 'null':
            return "N/A"
        # Clean up and return first few companies
        companies = companies_str.replace('[', '').replace(']', '').replace("'", "")
        company_list = [c.strip() for c in companies.split(',')]
        return ', '.join(company_list[:3]) if company_list else "N/A"
    
    def create_movie_key(self, movie: Dict) -> str:
        """Create a unique key for movie comparison"""
        title = self.normalize_title(movie.get('Title', ''))
        year = movie.get('Year', '')
        return f"{title}|{year}"
    
    def find_duplicates_and_merge(self):
        """Find unique movies and merge datasets"""
        print("🔍 Checking for duplicates and merging datasets...")
        
        # Create set of existing movie keys
        existing_keys = set()
        for movie in self.existing_movies:
            key = self.create_movie_key(movie)
            existing_keys.add(key)
        
        # Track what we add
        new_movies = []
        
        # Check each TMDB movie
        for tmdb_movie in self.tmdb_movies:
            key = self.create_movie_key(tmdb_movie)
            
            if key in existing_keys:
                self.duplicates_found += 1
            else:
                new_movies.append(tmdb_movie)
                existing_keys.add(key)
                self.movies_added += 1
        
        # Combine all movies
        all_movies = self.existing_movies + new_movies
        
        print(f"✅ Found {self.duplicates_found} duplicates")
        print(f"✅ Adding {self.movies_added} new unique movies")
        print(f"✅ Total movies after merge: {len(all_movies)}")
        
        return all_movies
    
    def create_backup(self):
        """Create backup of existing movies file"""
        print("💾 Creating backup...")
        try:
            if EXISTING_MOVIES_FILE.exists():
                import shutil
                shutil.copy2(EXISTING_MOVIES_FILE, BACKUP_FILE)
                print(f"✅ Backup created: {BACKUP_FILE}")
                return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def save_merged_movies(self, movies: List[Dict]):
        """Save merged movies to JSON file"""
        print("💾 Saving merged movie collection...")
        
        try:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(movies, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved {len(movies)} movies to {OUTPUT_FILE}")
            return True
        except Exception as e:
            print(f"❌ Error saving movies: {e}")
            return False
    
    def generate_report(self):
        """Generate a summary report"""
        report = f"""
📊 TMDB Movie Integration Report
{"="*50}
📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 Statistics:
• Existing movies: {len(self.existing_movies):,}
• TMDB movies processed: {len(self.tmdb_movies):,}
• Duplicates found: {self.duplicates_found:,}
• New movies added: {self.movies_added:,}
• Total movies after merge: {len(self.existing_movies) + self.movies_added:,}

📁 Files:
• Source: {TMDB_CSV_FILE}
• Output: {OUTPUT_FILE}
• Backup: {BACKUP_FILE}

✅ Integration completed successfully!
"""
        print(report)
        
        # Save report to file
        report_file = BASE_DIR / f"merge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"📄 Report saved to: {report_file}")
        except Exception as e:
            print(f"⚠️ Could not save report: {e}")
    
    def run(self):
        """Main execution function"""
        print("🎬 TMDB Movie Dataset Integration")
        print("="*50)
        
        # Step 1: Load existing movies
        if not self.load_existing_movies():
            return False
        
        # Step 2: Load TMDB movies
        if not self.load_tmdb_movies():
            return False
        
        # Step 3: Create backup
        if not self.create_backup():
            return False
        
        # Step 4: Find duplicates and merge
        merged_movies = self.find_duplicates_and_merge()
        
        # Step 5: Save merged collection
        if not self.save_merged_movies(merged_movies):
            return False
        
        # Step 6: Generate report
        self.generate_report()
        
        return True

def main():
    """Main function"""
    merger = MovieMerger()
    success = merger.run()
    
    if success:
        print("\n🎉 Movie integration completed successfully!")
    else:
        print("\n❌ Movie integration failed!")
    
    return success

if __name__ == "__main__":
    main()
