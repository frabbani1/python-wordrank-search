# python-wordrank-search (News Pulse)

A Python command-line tool that fetches the latest news articles on the topics you choose, saves them to a local SQLite database, and analyzes them. It prints reports, generates charts, ranks the most common words in headlines, and serves a simple web dashboard.

News data comes from the [newsdata.io](https://newsdata.io) API.

## Features

- **Fetch news** by topic from the command line or from a topics file
- **Store articles** locally in a SQLite database (`news.db`)
- **Reports**: print every stored article, or a pandas summary with totals, sample titles, and keyword coverage
- **Charts**: articles with vs. without keywords, and title length distribution
- **Word ranking**: top 15 most frequent words in headlines, with common filler words removed
- **Scheduling**: run the full pipeline once, or repeat it every day at a set time
- **Web dashboard**: a Flask page showing the article count and top words

## Requirements

- Python 3.11+
- A free API key from [newsdata.io](https://newsdata.io)

## Installation

1. Clone the repo:
```bash
   git clone https://github.com/<frabbani1>/python-wordrank-search.git
   cd python-wordrank-search
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv .venv
   source .venv/bin/activate        # macOS/Linux
   .venv\Scripts\activate           # Windows
```

3. Install the dependencies:
```bash
   pip install -r requirements.txt
```

4. Create a `.env` file in the project root with your API key:
```
   API_KEY=your_newsdata_io_key_here
```

## Usage

| Command | What it does |
|---|---|
| `python index.py --fetch --topic "tech, space"` | Fetch articles for comma-separated topics |
| `python index.py --fetch` | Fetch articles, entering topics one at a time (`q` to finish) |
| `python index.py --report` | Print every article in the database |
| `python index.py --pandas-report` | Print a summary: total articles, sample titles, keyword count |
| `python index.py --charts` | Save the keyword and title length charts as PNGs |
| `python index.py --words` | Save a chart of the 15 most common headline words |
| `python index.py --schedule` | Run the full pipeline once now, using the topics in `input.txt` |
| `python index.py --repeat` | Run the full pipeline every day at 08:00 |
| `python index.py --repeat 14:30` | Run the full pipeline every day at 14:30 (24-hour time) |
| `python index.py --web` | Launch the dashboard at http://127.0.0.1:5000 |

### Generated files

- `news.db`: SQLite database of saved articles
- `articles_with_without_keywords.png`
- `article_title_length_distribution.png`
- `most_frequent_words.png`

## Project Structure

```
python-wordrank-search/
├── index.py              # Main script: CLI, analysis, scheduling, Flask app
├── News.py               # News class: saves articles to the database
├── templates/
│   └── dashboard.html    # Web dashboard template
├── requirements.txt
├── .env                  # Your API key (don't commit this)
└── input.txt             # Topics for scheduled runs
```

## Notes

- Add `.env` and `news.db` to your `.gitignore` so your API key and local data stay private.
- The newsdata.io free tier has a daily request limit, so fetching many topics at once can use it up quickly.

## Author

Faiz Rabbani