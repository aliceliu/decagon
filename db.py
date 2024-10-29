import sqlite3

db_name = "docs.db"

def create_urls_table():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL UNIQUE, content TEXT)")

def drop_urls_table():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE urls")

def get_docs():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url, content FROM urls")
        results = cursor.fetchall()
        docs = {}
        for r in results:
            url, content = r
            docs[url] = content
        return docs

def store_docs(docs: dict[str, str]) -> None:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        for url, doc in docs.items():
            cursor.execute("INSERT INTO urls (url, content) VALUES (?, ?)", (url, doc))
        conn.commit()