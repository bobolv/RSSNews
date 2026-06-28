from db import get_conn, init_db


def main():
    init_db()
    conn = get_conn()
    c = conn.cursor()

    print("news columns:")
    for row in c.execute("PRAGMA table_info(news)").fetchall():
        print(tuple(row))

    count = c.execute("SELECT COUNT(*) FROM news").fetchone()[0]
    print(f"news count: {count}")
    conn.close()


if __name__ == "__main__":
    main()
