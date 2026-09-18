import json
import os

import requests
from dotenv import load_dotenv


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

def extract_articles(raw_json):
    articles = []
    for article in raw_json.get("results",[]):
        articles.append({
            "article_id" : article["article_id"] ,
            "link" : article["link"],
            "description" : article["description"] ,
            "title" : article["title"] ,
            "keywords" : article["keywords"]
        })
        return articles

if __name__ == "__main__":
    query = input("Enter your search query: ")
    articles = extract_articles(fetch_news(query, load_api_key()))
    print(json.dumps(articles, indent = 4))