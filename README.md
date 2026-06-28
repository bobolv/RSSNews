# RSSNews

RSSNews is a small Flask app for collecting RSS articles, saving favorites, and generating Obsidian-friendly summary notes.

## Features

- Fetch RSS items into SQLite.
- Review news in a compact web UI.
- Favorite articles and add them to a knowledge base.
- Generate summary-only Markdown notes instead of saving full article text.
- Write source links and content-based English/Chinese tags into Obsidian frontmatter.
- Select which RSS sources to fetch and add new RSS sources from the web UI.
- Run locally or with Docker Compose.

## Local Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

Fetch RSS from the web UI with "Get latest RSS", or from the command line:

```powershell
python rss_fetch.py
```

## Docker Run

Create `.env` first:

```powershell
copy .env.example .env
```

Fill these values if you want AI summaries:

```text
ARK_API_KEY=your_api_key
ARK_MODEL=your_model
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
FETCH_ON_STARTUP=0
```

`FETCH_ON_STARTUP` defaults to `0`. This is recommended because RSS fetching can be slow during container startup. Use the web UI to fetch selected sources after the app is running.

Start:

```powershell
docker compose up -d --build
```

Check:

```powershell
docker compose ps
docker compose logs -f
```

## Volumes

For local, portable storage:

```yaml
volumes:
  - ./data:/data
  - ./knowledge:/data/knowledge
```

For a Windows shared drive:

```yaml
volumes:
  - ./data:/data
  - Z:/RSS/knowledge:/data/knowledge
```

For Linux:

```yaml
volumes:
  - ./data:/data
  - /mnt/rss/knowledge:/data/knowledge
```

Inside the container:

- Database: `/data/rss_news.db`
- Knowledge notes: `/data/knowledge/<feed>/<article>_summary.md`

## Useful Commands

```powershell
python migrate.py
python checkDB.py
python summary.py file.md
docker compose exec rssnews python rss_fetch.py
```
