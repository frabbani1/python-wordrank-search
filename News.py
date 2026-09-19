import sqlite3


class News:
    def __init__(self, articles, db_path="news.db"):
        self.articles = articles
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS articles (article_id TEXT PRIMARY KEY, link TEXT, title TEXT, description TEXT, keywords TEXT)"
        )
        self.conn.commit()

    def save_articles(self):

        for article in self.articles:
            keywords = article['keywords']
            if isinstance(keywords, list):
                keywords = ', '.join(keywords)
                
            self.conn.execute(
                "INSERT OR REPLACE INTO articles (article_id, link, title, description, keywords) VALUES (?,?,?,?,?)",
                (
                    article["article_id"],
                    article["link"],
                    article["title"],
                    article["description"],
                    keywords
                )
            )
            self.conn.commit()

    def close_connection(self):
        self.conn.close()
