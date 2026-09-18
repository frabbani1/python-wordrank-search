import json
import os

import requests
from dotenv import load_dotenv

query = input("Enter your search query: ")




#loads up the api key
def load_api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key

#fetches news based on query
def fetch_news(query, api_key):
    url = f"https://newsdata.io/api/1/latest?apikey={api_key}&q={query}"
    response = requests.get(url)
    return response.json()

with open("news.json", "w") as f:
    json.dump(fetch_news(query, load_api_key()), f, indent=4)