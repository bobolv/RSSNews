import os
import threading

from flask import Flask, redirect, render_template, request, url_for

from article_fetch import fetch_and_save
from db import get_conn, init_db
from rss_fetch import add_feed, feed_options, fetch_feeds


init_db()
app = Flask(__name__)


def should_fetch_on_startup():
    return os.getenv("FETCH_ON_STARTUP", "1").lower() not in {"0", "false", "no"}


if should_fetch_on_startup():
    def fetch_on_startup():
        try:
            fetch_feeds()
        except Exception as exc:
            print(f"Startup RSS fetch failed: {exc}")

    threading.Thread(target=fetch_on_startup, daemon=True).start()


def can_retry(item):
    summary = item["summary"] or ""
    failure_words = (
        "[SUMMARY_FAILED:",
        "[SUMMARY_SKIPPED:",
        "[SAVE_FAILED:",
        "[FETCH_FAILED:",
        "\u5931\u8d25",
        "\u6458\u8981\u751f\u6210\u5931\u8d25",
        "\u6f6e\u8fa8\u89e6",
    )
    return item["status"] != 2 or any(word in summary for word in failure_words)


def feed_color(feed_name):
    return sum(ord(char) for char in (feed_name or "")) % 10


def redirect_to(endpoint, news_id=None, **values):
    target = url_for(endpoint, **values)
    if news_id is not None:
        target = f"{target}#news-{news_id}"
    return redirect(target)


@app.route("/")
def index():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT id, feed_name, title, link, published, favorite, status, markdown_path, summary
        FROM news
        ORDER BY id DESC
        """
    )
    news_list = []
    for row in c.fetchall():
        item = dict(row)
        item["retryable"] = can_retry(row)
        item["feed_color"] = feed_color(item["feed_name"])
        news_list.append(item)
    conn.close()
    return render_template("index.html", news_list=news_list)


@app.post("/favorites/<int:news_id>")
def favorite(news_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        UPDATE news
        SET favorite=1,
            status=CASE WHEN status=2 THEN 2 ELSE 1 END
        WHERE id=?
        """,
        (news_id,),
    )
    conn.commit()
    conn.close()
    return redirect_to("index", news_id)


@app.post("/unfavorite/<int:news_id>")
def unfavorite(news_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        UPDATE news
        SET favorite=0,
            status=CASE WHEN status=2 THEN 2 ELSE 0 END
        WHERE id=?
        """,
        (news_id,),
    )
    conn.commit()
    conn.close()
    next_page = request.args.get("next", "index")
    if next_page == "favorites":
        return redirect_to("favorites", news_id)
    return redirect_to("index", news_id)


@app.route("/favorites")
def favorites():
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        """
        SELECT id, feed_name, title, link, published, status, markdown_path, summary
        FROM news
        WHERE favorite=1
        ORDER BY id DESC
        """
    )
    news_list = []
    for row in c.fetchall():
        item = dict(row)
        item["retryable"] = can_retry(row)
        news_list.append(item)
    conn.close()
    return render_template("favorites.html", news_list=news_list)


@app.post("/fetch/<int:news_id>")
def fetch_article(news_id):
    fetch_and_save(news_id)
    next_page = request.args.get("next", "favorites")
    if next_page == "index":
        return redirect_to("index", news_id)
    return redirect_to("favorites", news_id)


@app.get("/refresh")
def refresh():
    return render_template("refresh.html", feeds=feed_options(), message=request.args.get("message", ""))


@app.post("/refresh/fetch")
def refresh_fetch():
    selected = request.form.getlist("feeds")
    if not selected:
        return redirect(url_for("refresh", message="Please select at least one RSS source"))
    result = fetch_feeds(selected)
    return redirect(
        url_for("refresh", message=f"RSS fetch complete: inserted {result['total_new']} new entries")
    )


@app.post("/feeds/add")
def feeds_add():
    try:
        add_feed(request.form.get("name", ""), request.form.get("url", ""))
        message = "RSS source added"
    except ValueError as exc:
        message = str(exc)
    return redirect(url_for("refresh", message=message))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
