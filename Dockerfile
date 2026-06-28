FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DB_FILE=/data/rss_news.db \
    KNOWLEDGE_DIR=/data/knowledge

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libxml2 libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /data/knowledge

EXPOSE 5000

CMD ["python", "app.py"]
