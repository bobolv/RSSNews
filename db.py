import os
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_FILE = Path(os.getenv("DB_FILE", BASE_DIR / "data" / "rss_news.db"))
DB_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_name TEXT,
            title TEXT,
            link TEXT UNIQUE,
            published TEXT,
            favorite INTEGER DEFAULT 0,
            markdown_path TEXT,
            summary TEXT,
            status INTEGER DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS feed_state (
            feed_name TEXT PRIMARY KEY,
            feed_url TEXT,
            last_fetched_at DATETIME,
            last_entry_count INTEGER DEFAULT 0,
            last_new_count INTEGER DEFAULT 0,
            last_error TEXT
        )
        """
    )
    ensure_columns(conn)
    ensure_feed_state_columns(conn)
    conn.commit()
    conn.close()


def ensure_columns(conn):
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(news)").fetchall()}
    migrations = {
        "favorite": "ALTER TABLE news ADD COLUMN favorite INTEGER DEFAULT 0",
        "markdown_path": "ALTER TABLE news ADD COLUMN markdown_path TEXT",
        "summary": "ALTER TABLE news ADD COLUMN summary TEXT",
        "status": "ALTER TABLE news ADD COLUMN status INTEGER DEFAULT 0",
        "created_at": "ALTER TABLE news ADD COLUMN created_at DATETIME",
    }
    for column, sql in migrations.items():
        if column not in columns:
            conn.execute(sql)


def ensure_feed_state_columns(conn):
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(feed_state)").fetchall()}
    migrations = {
        "feed_url": "ALTER TABLE feed_state ADD COLUMN feed_url TEXT",
        "last_fetched_at": "ALTER TABLE feed_state ADD COLUMN last_fetched_at DATETIME",
        "last_entry_count": "ALTER TABLE feed_state ADD COLUMN last_entry_count INTEGER DEFAULT 0",
        "last_new_count": "ALTER TABLE feed_state ADD COLUMN last_new_count INTEGER DEFAULT 0",
        "last_error": "ALTER TABLE feed_state ADD COLUMN last_error TEXT",
    }
    for column, sql in migrations.items():
        if column not in columns:
            conn.execute(sql)


def save_news(feed_name, title, link, published):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        INSERT OR IGNORE INTO news (feed_name, title, link, published)
        VALUES (?, ?, ?, ?)
        """,
        (feed_name, title, link, published),
    )
    inserted = c.rowcount
    conn.commit()
    conn.close()
    return inserted
