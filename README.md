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

Make sure Docker Desktop is running and is using Linux containers. Create `.env` first:

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

If a local `python app.py` instance is already using port 5000, stop it before running Compose.

Check:

```powershell
docker compose ps
docker compose logs --tail 100 rssnews
```

Open `http://127.0.0.1:5000` after the container reports `healthy`.

To build and run without Compose:

```powershell
docker build -t rssnews:local .
docker run -d --name rssnews --restart unless-stopped `
  -p 5000:5000 --env-file .env `
  -v "${PWD}/data:/data" `
  -v "${PWD}/knowledge:/data/knowledge" `
  rssnews:local
```

Stop or remove the Compose container:

```powershell
docker compose stop
docker compose down
```

## Tailscale Access

Docker Desktop may only expose the published port reliably on localhost. To make the app available
privately to other devices in the same tailnet, forward the Tailscale port to the local container:

```powershell
tailscale serve --bg --tcp=5000 tcp://127.0.0.1:5000
tailscale serve --bg --http=80 http://127.0.0.1:5000
tailscale serve status
```

For browser access, prefer the MagicDNS URL shown by `tailscale serve status`, without a port,
for example `http://home-desktop.tailefd88c.ts.net/`. The raw Tailscale IP remains available on
port 5000 for clients that support it.
The background Serve configuration persists across Tailscale restarts. To disable it:

```powershell
tailscale serve --tcp=5000 off
tailscale serve --http=80 off
```

## Volumes

Docker Desktop uses local, portable storage by default:

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
