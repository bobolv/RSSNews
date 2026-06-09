print("=== article_fetch start ===")

import os
import trafilatura
import sqlite3
from db import get_conn
from dotenv import load_dotenv
load_dotenv()

print("trafilatura imported")

print("API_KEY =", os.getenv("ARK_API_KEY"))
print("MODEL =", os.getenv("ARK_MODEL"))

KNOWLEDGE_DIR = "knowledge"
os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

def fetch_and_save(news_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM news WHERE id=?", (news_id,))
    news = c.fetchone()
    if not news:
        conn.close()
        return None

    url = news["link"]
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        conn.close()
        return None

    content = trafilatura.extract(downloaded, output_format="markdown", include_comments=False)
    if not content:
        conn.close()
        return None

    # 保存 Markdown
    filename = f"{news_id}_{news['title'][:50].replace(' ','_').replace('/','_')}.md"
    path = os.path.join(KNOWLEDGE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    # AI 摘要（示例使用 openai GPT-3/4）
    try:
        from openai import OpenAI 
        #openai.api_key = os.getenv("ARK_API_KEY")
        client = OpenAI(api_key=os.getenv("ARK_API_KEY"),base_url="https://ark.cn-beijing.volces.com/api/v3")
        resp = client.chat.completions.create(
            model=os.getenv("ARK_MODEL"),
            messages=[
                {"role":"system","content":"你是一个新闻摘要生成器"},
                {"role":"user","content":f"请对以下文章生成300字左右的摘要:\n\n{content}"}
            ]
        )
        summary = resp.choices[0].message.content.strip()
    except Exception as e:
        summary = f"[摘要生成失败: {e}]"
    #summary = "[摘要功能未启用]"

    # 更新数据库
    c.execute("""
        UPDATE news 
        SET markdown_path=?, summary=?, status = 2
        WHERE id=?
    """, (path, summary, news_id))
    conn.commit()
    conn.close()
    return path, summary