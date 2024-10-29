import time

from bs4 import BeautifulSoup
import requests


BASE_URL = "https://www.notion.so"
def scrape_docs() -> None:
    to_scrape = [BASE_URL + "/help"]
    seen = set(BASE_URL + "/help")
    docs = {}
    while to_scrape:
        url = to_scrape.pop(0)
        print(f"Scraping {url}...")
        response = requests.get(url)
        if not response.ok:
            print(f"Encountered error status {response.status_code} for url {url}")
            continue

        docs[url] = response.text
        soup = BeautifulSoup(response.text, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True)]
        for link in links:
            if should_parse_link(link):
                # Drop hashtags
                additional_url = BASE_URL + link.split("#")[0]
                if additional_url not in seen:
                    to_scrape.append(additional_url)
                    seen.add(additional_url)
        time.sleep(0.1)
    return docs

def should_parse_link(link: str):
    if not link.startswith("/help"):
        return False
    if link.startswith("/help/notion-academy"):
        return False
    return True