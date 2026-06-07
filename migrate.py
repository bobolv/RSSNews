# migrate.py

import sqlite3

conn = sqlite3.connect("data/rss_news.db")

c = conn.cursor()

columns = [x[1] for x in c.execute(
    "PRAGMA table_info(news)"
).fetchall()]

if "markdown_path" not in columns:
    c.execute("""
    ALTER TABLE news
    ADD COLUMN markdown_path TEXT
    """)

if "status" not in columns:
    c.execute("""
    ALTER TABLE news
    ADD COLUMN status INTEGER DEFAULT 0
    """)

conn.commit()

print("Migration OK")

conn.close()