
import requests, json, time, csv

api_key = '984b4107'
all_movies = []

with open('imdb_clean.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        title = row['title']
        resp = requests.get(f"http://www.omdbapi.com/?t={title}&apikey={api_key}")
        data = resp.json()
        if data.get("Response") == "True":
            all_movies.append(data)
        time.sleep(0.2)

with open('all_10000_movies.json','w',encoding='utf-8') as f:
    json.dump(all_movies, f, indent=4)
