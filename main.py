from chunker import generate_chunks
from db import create_urls_table, drop_urls_table, get_docs, store_docs
from scraper import scrape_docs

def main():
    # Uncomment below to force scraping
    # drop_urls_table()
    create_urls_table()
    docs = get_docs()
    if not docs:
        docs = scrape_docs()
        store_docs(docs)
    final_chunks = []
    for url, doc in docs.items():
        chunks = generate_chunks(doc)
        final_chunks += chunks
    print(final_chunks)
    return final_chunks

if __name__ == "__main__":
    main()
