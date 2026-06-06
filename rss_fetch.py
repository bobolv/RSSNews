import os
import yaml
import feedparser
import sqlite3
#from db import save_news, init_db

#项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#RSS 配置文件路径
FEEDS_FILE = os.path.join(BASE_DIR, "feeds.yaml")
#数据库路径
DB_FILE = os.path.join(BASE_DIR, "data/rss_news.db")

# # 初始化数据库
# init_db()

# 加载配置文件
with open(FEEDS_FILE, "r", encoding="utf-8") as f:
    feeds_config = yaml.safe_load(f)

# with open("feeds.yaml", "r", encoding="utf-8") as f:
#     feeds_config = yaml.safe_load(f)

def save_news(feed_name, title, link, published):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feed_name TEXT,
            title TEXT,
            link TEXT,
            published TEXT
        )
    """)
    c.execute("""
        INSERT OR IGNORE INTO news (feed_name, title, link, published)
        VALUES (?, ?, ?, ?)
    """, (feed_name, title, link, published))

    inserted = c.rowcount

    conn.commit()
    conn.close()

    return inserted

new_count = 0

for feed in feeds_config["feeds"]:
    print(f"抓取 {feed['name']}")
    d = feedparser.parse(feed["url"])
    print(f"发现 {len(d.entries)} 条新闻")
    for entry in d.entries:
        new_count += save_news(
            feed['name'],
            entry.title,
            entry.link,
            getattr(entry, "published", "")
        )
    print(f"{feed['name']}: 新增 {new_count} 条")
