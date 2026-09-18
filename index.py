from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

api_key = os.getenv("API_KEY")

query = input("Enter your search query: ")
url = f"https://newsdata.io/api/1/latest?apikey={api_key}&q={query}"
response = requests.get(url)

with open("output.json", "w") as f:
    json.dump(response.json(), f)
