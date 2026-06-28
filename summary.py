import argparse
from pathlib import Path

from article_fetch import summarize


def main():
    parser = argparse.ArgumentParser(description="为 Markdown 文件生成摘要")
    parser.add_argument("markdown_path", help="Markdown 文件路径")
    args = parser.parse_args()

    path = Path(args.markdown_path)
    content = path.read_text(encoding="utf-8")
    result = summarize(content)
    if isinstance(result, dict):
        print(result["summary"])
        if result.get("tags"):
            print("\nTags:")
            for tag in result["tags"]:
                print(f"- {tag.get('en', '')} / {tag.get('zh', '')}")
    else:
        print(result)


if __name__ == "__main__":
    main()
