import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import csv
import time

BASE_URL = "https://connect.mq.edu.au/s/"
START_URL = "https://connect.mq.edu.au/s/"
visited = set()
MAX_PAGES = 300  # Increase if needed

def infer_category(url):
    path_parts = urlparse(url).path.strip("/").split("/")
    for part in path_parts:
        if part and part.lower() not in ["home", "study"]:
            return part.capitalize()
    return "General"

def scrape_page(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Get title
        title = soup.find("h1") or soup.find("title")
        title_text = title.get_text(strip=True) if title else "Untitled"

        # Get content
        main = soup.find("main") or soup
        paragraphs = main.find_all(["p", "li"])
        text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Get all new links
        all_links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
        internal_links = [
            link for link in all_links
            if link.startswith(BASE_URL) and ".pdf" not in link and "#" not in link
        ]

        category = infer_category(url)
        return {
            "category": category,
            "title": title_text,
            "answer": text,
            "url": url
        }, internal_links

    except Exception as e:
        print(f"⚠️ Failed at {url}: {e}")
        return None

def crawl_all(start_url):
    to_visit = [start_url]
    data = []

    while to_visit and len(visited) < MAX_PAGES:
        url = to_visit.pop(0)
        if url in visited:
            continue
        print(f"🔍 Visiting: {url}")
        visited.add(url)

        result = scrape_page(url)
        if result:
            article, links = result
            if article["answer"]:
                data.append(article)
            for link in links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
        time.sleep(1)

    return data

if __name__ == "__main__":
    results = crawl_all(START_URL)

    with open("mq_connect_full_site.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "title", "answer", "url"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Done! Scraped {len(results)} pages from the full site.")