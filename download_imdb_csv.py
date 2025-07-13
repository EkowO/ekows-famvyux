import requests
import os
import pandas as pd

def download_imdb_csv():
    """Download IMDB Top 1000 Movies CSV from GitHub"""
    
    # GitHub raw URL for the CSV file
    url = "https://raw.githubusercontent.com/peetck/IMDB-Top1000-Movies/master/IMDB-Movie-Data.csv"
    
    # Local file path
    local_file = r"c:\Users\edakw\Downloads\fam\ekows-famvyux\get movies\IMDB-Movie-Data.csv"
    
    print("🌐 Downloading IMDB Top 1000 Movies CSV...")
    print(f"📥 URL: {url}")
    print(f"💾 Saving to: {local_file}")
    
    try:
        # Download the file
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_file), exist_ok=True)
        
        # Save the file
        with open(local_file, 'wb') as f:
            f.write(response.content)
        
        print("✅ Download completed successfully!")
        
        # Read and display some info about the CSV
        try:
            df = pd.read_csv(local_file)
            print(f"📊 File contains {len(df)} movies")
            print(f"📋 Columns: {', '.join(df.columns.tolist())}")
            
            # Show first few rows
            print("\n🎬 First 5 movies:")
            print(df.head()[['Title', 'Year', 'Rating', 'Genre']].to_string(index=False))
            
            # Show year range
            if 'Year' in df.columns:
                min_year = df['Year'].min()
                max_year = df['Year'].max()
                print(f"\n📅 Year range: {min_year} - {max_year}")
                
            # Show rating range
            if 'Rating' in df.columns:
                min_rating = df['Rating'].min()
                max_rating = df['Rating'].max()
                print(f"⭐ Rating range: {min_rating} - {max_rating}")
                
        except Exception as e:
            print(f"⚠️ Could not analyze CSV content: {e}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error downloading file: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = download_imdb_csv()
    if success:
        print("\n🎉 Ready to import movies from this CSV!")
        print("💡 You can now use this file to add more movies to your database.")
    else:
        print("\n💔 Download failed. Please check your internet connection and try again.")
