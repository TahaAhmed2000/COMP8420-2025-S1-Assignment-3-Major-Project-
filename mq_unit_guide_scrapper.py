from playwright.sync_api import sync_playwright
import csv
import re
import time
import pandas as pd

mq_units = pd.read_csv('mq_unit_guide_links_2025.csv')

unit_urls = mq_units['url'].tolist()

def scrape_with_playwright(url, page):
    try:
        page.goto(url, timeout=30000)
        page.wait_for_selector("div#unit-guide-content", timeout=10000)
        time.sleep(2)  # ensure JS-loaded content appears

        # Extract unit code and title from <h1>
        h1_text = page.locator("header.unit-guide-header-container h1").first.text_content().strip()
        match = re.match(r"([A-Z]{4}\d{4})\s*[-–]?\s*(.+)", h1_text)
        unit_code = match.group(1) if match else ""
        unit_title = match.group(2) if match else h1_text

        # Extract content from all major sections
        sections = page.locator("div#unit-guide-content section").all()
        all_content = []

        for section in sections:
            try:
                heading = section.locator("h2").first.text_content().strip()
                body = section.inner_text().strip()
                all_content.append(f"## {heading}\n{body}")
            except:
                continue

        return {
            "category": "Unit Guide",
            "title": unit_title,
            "answer": "\n\n".join(all_content),
            "url": url
        }

    except Exception as e:
        print(f"❌ Failed to scrape {url}: {e}")
        return None

def main():
    scraped_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        for url in unit_urls:
            print(f"🔍 Scraping: {url}")
            data = scrape_with_playwright(url, page)
            if data:
                scraped_data.append(data)
            time.sleep(1)  # polite crawling

        browser.close()

    # ✅ Save to unified CSV format
    with open("mq_unit_guides_final.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "title", "answer", "url"])
        writer.writeheader()
        writer.writerows(scraped_data)

    print(f"\n✅ Done! {len(scraped_data)} unit guides saved to mq_unit_guides_final.csv")

if __name__ == "__main__":
    main()