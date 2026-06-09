from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("ARK_API_KEY"),
    base_url="https://ark.cn-beijing.volces.com/api/v3"
)

def summarize_markdown(content):

    response = client.chat.completions.create(
        model=os.getenv("ARK_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你是技术情报分析助手。"
            },
            {
                "role": "user",
                "content": f"""
                请阅读以下文章并输出：
                    # 一句话总结
                    # 三个关键观点
                    # 对运维工程师的价值
                    文章内容：{content[:12000]}
                """
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

summary = summarize_markdown(content)