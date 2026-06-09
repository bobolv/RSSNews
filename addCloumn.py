import sqlite3

DB_PATH = "data/rss_news.db"

def add_column_if_not_exists(conn, table_name, column_name, column_type="TEXT"):
    # 获取表的现有列
    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    if column_name not in columns:
        print(f"Adding column '{column_name}' to table '{table_name}'")
        conn.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT CURRENT_TIMESTAMP")
        conn.commit()
    else:
        print(f"Column '{column_name}' already exists in table '{table_name}'")

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        #add_column_if_not_exists(conn, "news", "markdown_path", "TEXT")
        #add_column_if_not_exists(conn, "news", "summary", "TEXT")
        add_column_if_not_exists(conn, "news", "created_at", "DATETIME")
        print("Database update complete.")
    except Exception as e:
        print("Error updating database:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()