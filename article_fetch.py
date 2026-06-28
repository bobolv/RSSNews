import json
import os
import re
from pathlib import Path
from datetime import datetime

import trafilatura
from dotenv import load_dotenv

from db import get_conn


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_KNOWLEDGE_DIR = Path(r"Z:\RSS\knowledge") if os.name == "nt" else Path("/data/knowledge")
KNOWLEDGE_DIR = Path(os.getenv("KNOWLEDGE_DIR", DEFAULT_KNOWLEDGE_DIR))

SUMMARY_SKIPPED = "[SUMMARY_SKIPPED: ARK_API_KEY or ARK_MODEL is not configured]"


def safe_name(value, fallback="untitled", max_length=80):
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value or "")
    value = re.sub(r"\s+", "_", value).strip("._ ")
    return (value or fallback)[:max_length]


def article_path(news):
    category = safe_name(news["feed_name"], "uncategorized", 60)
    title = safe_name(news["title"], f"article_{news['id']}", 90)
    directory = KNOWLEDGE_DIR / category
    directory.mkdir(parents=True, exist_ok=True)
    return directory / f"{news['id']}_{title}_summary.md"


def yaml_quote(value):
    return '"' + str(value or "").replace("\\", "\\\\").replace('"', '\\"') + '"'


def normalize_tag(value):
    value = (value or "").strip().replace("#", "")
    value = re.sub(r"\s+", "-", value)
    chars = []
    for char in value:
        if char == "-" or char == "_" or char.isalnum() or "\u4e00" <= char <= "\u9fff":
            chars.append(char)
    return "".join(chars)[:40]


def build_tags(tags):
    result = []
    for tag in tags or []:
        english = normalize_tag(tag.get("en", "")).lower()
        chinese = normalize_tag(tag.get("zh", ""))
        for value in (english, chinese):
            if value and value not in result:
                result.append(value)
    return result[:7]


def summary_note(news, summary, tags):
    tag_values = build_tags(tags)
    tag_lines = ["tags:", *[f"  - {tag}" for tag in tag_values]] if tag_values else ["tags: []"]
    return "\n".join(
        [
            "---",
            "rssnews_note: summary",
            f"title: {yaml_quote(news['title'])}",
            f"source: {yaml_quote(news['link'])}",
            f"feed: {yaml_quote(news['feed_name'])}",
            f"published: {yaml_quote(news['published'])}",
            f"created: {yaml_quote(datetime.now().isoformat(timespec='seconds'))}",
            *tag_lines,
            "---",
            "",
            f"# {news['title']}",
            "",
            "> [!info] \u539f\u6587\u94fe\u63a5",
            f"> [\u6253\u5f00\u539f\u6587]({news['link']})",
            "",
            "## \u6458\u8981",
            "",
            summary,
            "",
        ]
    )


def mark_failed(conn, news_id, message):
    conn.execute(
        """
        UPDATE news
        SET markdown_path=NULL, summary=?, status=3
        WHERE id=?
        """,
        (message, news_id),
    )
    conn.commit()


def parse_summary_result(raw):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {"summary": raw.strip(), "tags": []}

    summary = str(data.get("summary", "")).strip()
    tags = data.get("tags", [])
    if not isinstance(tags, list):
        tags = []

    clean_tags = []
    for tag in tags[:3]:
        if isinstance(tag, dict):
            clean_tags.append({"en": str(tag.get("en", "")), "zh": str(tag.get("zh", ""))})

    return {"summary": summary or raw.strip(), "tags": clean_tags}


def summarize(content):
    api_key = os.getenv("ARK_API_KEY")
    model = os.getenv("ARK_MODEL")
    if not api_key or not model:
        return SUMMARY_SKIPPED

    try:
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
        )
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "\u4f60\u662f\u4e00\u4e2a\u65b0\u95fb\u6458\u8981\u548c"
                        "\u77e5\u8bc6\u6807\u7b7e\u751f\u6210\u5668\u3002"
                        "\u53ea\u8f93\u51fa JSON\uff0c\u4e0d\u8981 markdown\u3002"
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "\u8bf7\u9605\u8bfb\u6587\u7ae0\uff0c\u8f93\u51fa JSON\uff1a"
                        '{"summary":"300\u5b57\u5de6\u53f3\u7684\u4e2d\u6587\u6458\u8981",'
                        '"tags":[{"en":"english-topic","zh":"\u4e2d\u6587\u6807\u7b7e"}]}'
                        "\u3002tags \u6839\u636e\u539f\u6587\u5185\u5bb9\u751f\u6210 2-3 \u4e2a\uff0c"
                        "en \u7528\u82f1\u6587\u5c0f\u5199\u77ed\u6807\u7b7e\uff0czh \u7528\u5bf9\u5e94\u4e2d\u6587\u6807\u7b7e\u3002"
                        f"\n\n\u6587\u7ae0\uff1a\n{content[:12000]}"
                    ),
                },
            ],
            temperature=0.3,
        )
        return parse_summary_result(resp.choices[0].message.content.strip())
    except Exception as exc:
        return f"[SUMMARY_FAILED: {exc}]"


def fetch_and_save(news_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE id=?", (news_id,))
    news = c.fetchone()
    if not news:
        conn.close()
        return None

    downloaded = trafilatura.fetch_url(news["link"])
    if not downloaded:
        mark_failed(conn, news_id, "[FETCH_FAILED: unable to download article]")
        conn.close()
        return None

    content = trafilatura.extract(
        downloaded,
        output_format="markdown",
        include_comments=False,
    )
    if not content:
        mark_failed(conn, news_id, "[FETCH_FAILED: unable to extract article content]")
        conn.close()
        return None

    result = summarize(content)
    if isinstance(result, str):
        if result.startswith(("[SUMMARY_FAILED:", "[SUMMARY_SKIPPED:")):
            mark_failed(conn, news_id, result)
            conn.close()
            return None
        result = {"summary": result, "tags": []}

    summary = result["summary"]
    tags = result.get("tags", [])
    if not summary:
        mark_failed(conn, news_id, "[SUMMARY_FAILED: empty summary]")
        conn.close()
        return None

    try:
        path = article_path(news)
        path.write_text(summary_note(news, summary, tags), encoding="utf-8")
    except OSError as exc:
        mark_failed(conn, news_id, f"[SAVE_FAILED: {exc}]")
        conn.close()
        return None

    c.execute(
        """
        UPDATE news
        SET markdown_path=?, summary=?, status=2
        WHERE id=?
        """,
        (str(path), summary, news_id),
    )
    conn.commit()
    conn.close()
    return path, summary
