import os
import trafilatura
import sqlite3
from db import get_conn

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

    # # AI 摘要（示例使用 openai GPT-3/4）
    # try:
    #     import openai
    #     openai.api_key = os.environ.get("OPENAI_API_KEY", "")
    #     resp = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {"role":"system","content":"你是一个新闻摘要生成器"},
    #             {"role":"user","content":f"请对以下文章生成200字左右的摘要:\n\n{content}"}
    #         ]
    #     )
    #     summary = resp.choices[0].message.content.strip()
    # except Exception as e:
    #     summary = f"[摘要生成失败: {e}]"
    summary = "[摘要功能未启用]"

    # 更新数据库
    c.execute("""
        UPDATE news 
        SET markdown_path=?, summary=? 
        WHERE id=?
    """, (path, summary, news_id))
    conn.commit()
    conn.close()
    return path, summary