from db import get_conn, init_db


def main():
    init_db()
    conn = get_conn()
    columns = conn.execute("PRAGMA table_info(news)").fetchall()
    conn.close()

    print("Migration OK")
    for column in columns:
        print(f"- {column['name']} {column['type']}")


if __name__ == "__main__":
    main()
