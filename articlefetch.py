import argparse

import trafilatura


def main():
    parser = argparse.ArgumentParser(description="测试抓取指定 URL 的正文 Markdown")
    parser.add_argument("url", help="文章 URL")
    args = parser.parse_args()

    downloaded = trafilatura.fetch_url(args.url)
    content = trafilatura.extract(downloaded, output_format="markdown") if downloaded else ""
    print((content or "")[:4000])


if __name__ == "__main__":
    main()
