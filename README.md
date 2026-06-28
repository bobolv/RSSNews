# RSSNews

RSSNews 是一个 RSS 新闻抓取、收藏和知识库归档工具。它会从 `feeds.yaml` 读取 RSS 源，将新闻保存到 SQLite，并可把收藏文章提取为 Markdown，按来源分类保存到知识库目录。

## 功能

- 抓取 RSS 新闻并去重保存
- Flask Web 页面查看新闻和收藏
- 服务启动时自动抓取一次 RSS，也可在首页手动点击获取最新 RSS
- 收藏文章后抓取正文生成摘要，并将摘要保存为 Markdown 笔记
- 按 RSS 来源分类保存知识库文件
- 可选调用火山方舟兼容 OpenAI API 生成中文摘要
- 支持 Docker 部署和数据目录挂载

## 本地运行

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python rss_fetch.py
python app.py
```

访问：

```text
http://127.0.0.1:5000
```

默认 Windows 本地知识库目录是：

```text
Z:\RSS\knowledge
```

可通过环境变量覆盖：

```powershell
$env:KNOWLEDGE_DIR="D:\RSS\knowledge"
$env:DB_FILE="D:\RSS\rss_news.db"
```

## Docker 运行

先复制环境变量文件：

```powershell
copy .env.example .env
```

如果要生成摘要，在 `.env` 中填写：

```text
ARK_API_KEY=你的 API Key
ARK_MODEL=你的模型名
ARK_BASE_URL=https://ark.cn-beijing.volces.com/api/v3
FETCH_ON_STARTUP=1
```

如果不希望服务启动时自动抓取 RSS，把 `FETCH_ON_STARTUP` 改为 `0`。

启动：

```powershell
docker compose up -d --build
```

抓取 RSS：

```powershell
docker compose exec rssnews python rss_fetch.py
```

查看日志：

```powershell
docker compose logs -f
```

## 目录挂载

`docker-compose.yml` 默认挂载：

```yaml
./data:/data
Z:/RSS/knowledge:/data/knowledge
```

容器内：

- 数据库：`/data/rss_news.db`
- Markdown 知识库：`/data/knowledge/<RSS来源>/<文章摘要>.md`

宿主机 Windows 上对应：

- 数据库：项目目录 `data/rss_news.db`
- Markdown 知识库：`Z:\RSS\knowledge\<RSS来源>\<文章摘要>.md`

迁移到其他主机时，只需要调整 `docker-compose.yml` 里的第二个 volume。例如 Linux 主机：

```yaml
volumes:
  - ./data:/data
  - /mnt/rss/knowledge:/data/knowledge
```

## 常用脚本

```powershell
python rss_fetch.py      # 抓取 RSS
python migrate.py        # 初始化或迁移数据库
python checkDB.py        # 查看数据库结构和新闻数量
python summary.py file.md
```
