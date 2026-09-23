import sqlite3

import matplotlib

matplotlib.use("Agg")  # lets charts save without opening windows

import index


# ---------- helper: builds a small fake database for testing ----------
def make_test_db(path):
    conn = sqlite3.connect(path)
    conn.execute(
        "CREATE TABLE articles (article_id TEXT, link TEXT, description TEXT, title TEXT, keywords TEXT)"
    )
    conn.executemany(
        "INSERT INTO articles VALUES (?, ?, ?, ?, ?)",
        [
            (
                "1",
                "http://a.com",
                "desc",
                "NASA launches new rocket to the moon",
                "space",
            ),
            ("2", "http://b.com", "desc", "Ohio State wins big game at home", None),
            (
                "3",
                "http://c.com",
                "desc",
                "NASA plans another rocket launch soon",
                "space",
            ),
        ],
    )
    conn.commit()
    conn.close()


# ---------- extract_articles ----------
def test_extract_articles_normal():
    fake_json = {
        "results": [
            {
                "article_id": "1",
                "link": "x",
                "description": "d",
                "title": "t1",
                "keywords": ["k"],
            },
            {
                "article_id": "2",
                "link": "y",
                "description": "d",
                "title": "t2",
                "keywords": None,
            },
        ]
    }
    articles = index.extract_articles(fake_json)
    assert len(articles) == 2  # got both, not just the first
    assert articles[0]["title"] == "t1"


def test_extract_articles_no_results():
    assert index.extract_articles({}) == []
    assert index.extract_articles({"results": []}) == []


# ---------- load_topics ----------
def test_load_topics(tmp_path):
    file = tmp_path / "input.txt"
    file.write_text("tech\n\n  space  \n")
    assert index.load_topics(file) == [
        "tech",
        "space",
    ]  # blank lines and spaces removed


# ---------- fetch_news (fakes the API so no real request is made) ----------
def test_fetch_news(monkeypatch):
    class FakeResponse:
        def json(self):
            return {"status": "success", "results": []}

    monkeypatch.setattr(index.requests, "get", lambda url: FakeResponse())
    assert index.fetch_news("tech", "fake_key")["status"] == "success"


# ---------- charts and word ranking ----------
def test_make_charts_creates_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_test_db("news.db")
    index.make_charts("news.db")
    assert (tmp_path / "articles_with_without_keywords.png").exists()
    assert (tmp_path / "article_title_length_distribution.png").exists()


def test_word_frequency_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_test_db("news.db")
    index.word_frequency("news.db")
    assert (tmp_path / "most_frequent_words.png").exists()


# ---------- web dashboard ----------
def test_dashboard_loads(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    make_test_db("news.db")
    client = index.app.test_client()
    response = client.get("/")
    assert response.status_code == 200  # page loaded without crashing
    assert b"3" in response.data  # total article count shows up
