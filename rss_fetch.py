from datetime import datetime
from pathlib import Path

import feedparser
import yaml

from db import get_conn, init_db, save_news


BASE_DIR = Path(__file__).resolve().parent
FEEDS_FILE = BASE_DIR / "feeds.yaml"


def load_feeds():
    if not FEEDS_FILE.exists():
        return []
    with FEEDS_FILE.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("feeds", [])


def save_feeds(feeds):
    with FEEDS_FILE.open("w", encoding="utf-8") as f:
        yaml.safe_dump({"feeds": feeds}, f, allow_unicode=True, sort_keys=False)


def add_feed(name, url):
    name = (name or "").strip()
    url = (url or "").strip()
    if not name or not url:
        raise ValueError("Feed name and URL are required")

    feeds = load_feeds()
    existing_names = {feed["name"].casefold() for feed in feeds}
    existing_urls = {feed["url"].casefold() for feed in feeds}
    if name.casefold() in existing_names:
        raise ValueError("Feed name already exists")
    if url.casefold() in existing_urls:
        raise ValueError("Feed URL already exists")

    feeds.append({"name": name, "url": url})
    save_feeds(feeds)
    return {"name": name, "url": url}


def update_feed_state(feed, entry_count=0, new_count=0, error=None):
    conn = get_conn()
    conn.execute(
        """
        INSERT INTO feed_state (
            feed_name, feed_url, last_fetched_at, last_entry_count, last_new_count, last_error
        )
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(feed_name) DO UPDATE SET
            feed_url=excluded.feed_url,
            last_fetched_at=excluded.last_fetched_at,
            last_entry_count=excluded.last_entry_count,
            last_new_count=excluded.last_new_count,
            last_error=excluded.last_error
        """,
        (
            feed["name"],
            feed["url"],
            datetime.now().isoformat(timespec="seconds"),
            entry_count,
            new_count,
            error,
        ),
    )
    conn.commit()
    conn.close()


def feed_options():
    init_db()
    conn = get_conn()
    states = {
        row["feed_name"]: dict(row)
        for row in conn.execute("SELECT * FROM feed_state").fetchall()
    }
    conn.close()

    options = []
    for feed in load_feeds():
        item = dict(feed)
        item.update(states.get(feed["name"], {}))
        options.append(item)
    return options


def fetch_feeds(selected_names=None):
    init_db()
    selected = set(selected_names or [])
    feeds = [
        feed
        for feed in load_feeds()
        if not selected or feed["name"] in selected
    ]

    total_new = 0
    results = []

    for feed in feeds:
        feed_name = feed["name"]
        print(f"Fetching {feed_name}")

        try:
            parsed = feedparser.parse(feed["url"])
            entry_count = len(parsed.entries)
            error = parsed.bozo_exception if getattr(parsed, "bozo", False) else None

            feed_new = 0
            for entry in parsed.entries:
                feed_new += save_news(
                    feed_name,
                    entry.get("title", ""),
                    entry.get("link", ""),
                    entry.get("published", entry.get("updated", "")),
                )

            total_new += feed_new
            update_feed_state(feed, entry_count, feed_new, str(error) if error else None)
            results.append(
                {
                    "name": feed_name,
                    "entry_count": entry_count,
                    "new_count": feed_new,
                    "error": str(error) if error else "",
                }
            )
            print(f"{feed_name}: found {entry_count}, inserted {feed_new}")
        except Exception as exc:
            update_feed_state(feed, 0, 0, str(exc))
            results.append({"name": feed_name, "entry_count": 0, "new_count": 0, "error": str(exc)})
            print(f"{feed_name}: failed: {exc}")

    print(f"RSS fetch complete: inserted {total_new} new entries")
    return {"total_new": total_new, "results": results}


if __name__ == "__main__":
    fetch_feeds()
