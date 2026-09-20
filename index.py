import argparse
import os
import sqlite3
import time

import requests
from dotenv import load_dotenv

import News
import pandas as pd


# loads up the api key
def load_api_key():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key


# fetches news based on query
def fetch_news(query, api_key):
    url = f"https://newsdata.io/api/1/latest?apikey={api_key}&q={query}"
    response = requests.get(url)
    return response.json()


def extract_articles(raw_json):
    articles = []
    for article in raw_json.get("results", []):
        articles.append(
            {
                "article_id": article["article_id"],
                "link": article["link"],
                "description": article["description"],
                "title": article["title"],
                "keywords": article["keywords"],
            }
        )
        return articles


def get_topics():
    topics = []
    while True:
        topic = input("Enter topic: press q to quit: ")
        if topic.lower() == "q":
            break
        topics.append(topic)

    return topics


def run_topics(topics, articles):
    for topic in topics:
        articles.extend(extract_articles(fetch_news(topic, load_api_key())))
        news = News.News(
            articles,
        )
        news.save_articles()
        news.close_connection()
        print(f"saved {len(articles)} articles to the database")
        time.sleep(1)


def print_report():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM articles")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def report_pandas(db):
    conn = sqlite3.connect(db)
    df = pd.read_sql_query("SELECT * FROM articles", conn)

    if df.empty:
        print("No articles found in the database.")

    print("Total articles in the database:", len(df))
    print("Article(s) sample titles :")
    print(df["title"].head(5))
    print("number of articles with non-empty keywords:")
    print(df["keywords"].notna().sum())





if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="News Fetcher")
    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetches all news articles based on topic --topic provided",
    )
    parser.add_argument(
        "--report", action="store_true", help="Prints out all articles in the datadase"
    )
    parser.add_argument(
        "--topic", type=str, help="Topic(s) to fetch news for, seperated by commas"
    )
    parser.add_argument("--pandas-report", action = "store_true", help = "Prints out number of articles, number of articles per topic, and number of articles per source (top 5) using pandas")

    args = parser.parse_args()

    api_key = load_api_key()
    db = sqlite3.connect("news.db")

    if args.fetch:
        if args.topic:
            topics = [topic.strip() for topic in args.topic.split(",")]
        else:
            topics = get_topics()

        if not topics:
            print("No topics provided")
        else:
            articles = []
            run_topics(topics, articles)

    elif args.report:
        print_report()

    elif args.pandas_report:
        report_pandas("news.db")

    else:
        print("No action provided. Use --fetch, --report or --pandas-report.")

    db.close()
