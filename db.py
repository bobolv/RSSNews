import sqlite3
from pathlib import Path

DB_FILE = Path("data/rss_news.db")
DB_FILE.parent.mkdir(exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_name TEXT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            favorite INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def save_news(feed_name, title, link, published):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO news (feed_name, title, link, published) VALUES (?, ?, ?, ?)",
                  (feed_name, title, link, published))
    except sqlite3.IntegrityError:
        pass  # 已存在，不重复保存
    conn.commit()
    conn.close()