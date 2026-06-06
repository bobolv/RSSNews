# from flask import Flask, render_template
# import sqlite3

# app = Flask(__name__)
# DB_FILE = "data/rss_news.db"

# @app.route("/")
# def index():
#     conn = sqlite3.connect(DB_FILE)
#     c = conn.cursor()
#     c.execute("SELECT feed_name, title, link, published FROM news ORDER BY published DESC")
#     news_list = c.fetchall()
#     conn.close()
#     return render_template("index.html", news_list=news_list)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)

# app.py
from flask import Flask, render_template, redirect, url_for
# from flask import Flask, render_template
# from flask import redirect
import sqlite3
import os

# ------------------------------
# 1️⃣ 创建 Flask 应用实例
# ------------------------------
app = Flask(__name__)

# ------------------------------
# 2️⃣ 数据库路径
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "data", "rss_news.db")

# ------------------------------
# 3️⃣ 路由
# ------------------------------
@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, feed_name, title, link, published, favorite FROM news ORDER BY id DESC")
    news_list = c.fetchall()
    conn.close()

    # 调试用
    print("DEBUG news_list =", news_list[:3])

    return render_template("index.html", news_list=news_list)

@app.route("/favorites/<int:news_id>")
def favorite(news_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        UPDATE news
        SET favorite=1
        WHERE id=?
    """,(news_id,))

    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/unfavorite/<int:news_id>")
def unfavorite(news_id):

    conn = sqlite3.connect(DB_FILE)

    c = conn.cursor()

    c.execute("""
        UPDATE news
        SET favorite = 0
        WHERE id = ?
    """, (news_id,))

    conn.commit()

    conn.close()

    return redirect("/")

@app.route("/favorites")
def favorites():

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        SELECT id,
               feed_name,
               title,
               link,
               published
        FROM news
        WHERE favorite = 1
        ORDER BY id DESC
    """)

    news_list = c.fetchall()

    conn.close()

    return render_template(
        "favorites.html",
        news_list=news_list
    )

# ------------------------------
# 4️⃣ 启动
# ------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)