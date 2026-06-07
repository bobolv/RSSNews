# article_fetch.py

import trafilatura

url = "https://www.docker.com/blog/meet-gordon-dockers-ai-agent-for-your-entire-container-workflow/"

downloaded = trafilatura.fetch_url(url)

content = trafilatura.extract(
    downloaded,
    output_format="markdown"
)

print(content[:1000])
with open(
    "knowledge/test.md",
    "w",
    encoding="utf-8"
) as f:
    f.write(content)