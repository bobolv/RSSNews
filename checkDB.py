import sqlite3

conn = sqlite3.connect("data/rss_news.db")
c = conn.cursor()

# 查看字段
c.execute("PRAGMA table_info(news)")
for row in c.fetchall():
    print(row)

conn.close()