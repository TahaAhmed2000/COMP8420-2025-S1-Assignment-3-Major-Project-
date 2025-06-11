from playwright.sync_api import sync_playwright
import csv
import time
import re

# Define AskMQ categories (label + URL)
category_pages = {
    "Managing & Understanding My Course": "https://connect.mq.edu.au/s/topic/0TOMn0000002c7dOAA/managing-understanding-my-course",
    "Managing & Understanding My Enrolment": "https://connect.mq.edu.au/s/topic/0TOMn0000002c7eOAA/managing-understanding-my-enrolment",
    "Managing My Assessments, Exams & Results": "https://connect.mq.edu.au/s/topic/0TOMn0000002c7fOAA/managing-my-assessments-exams-results",
    "Managing My Details, Documents & Cards": "https://connect.mq.edu.au/s/topic/0TOMn0000002c7gOAA/managing-my-details-documents-cards",
    "Managing My Fees & Costs": "https://connect.mq.edu.au/s/topic/0TOMn0000002c7hOAA/managing-my-fees-costs",
    "Other Student Services, Links & Feedback": "https://connect.mq.edu.au/s/topic/0TOMn0000002iD3OAI/other-student-services-links-feedback"
    # You can add more categories here
}

ARTICLE_LINK_PATTERN = r'https://connect\.mq\.edu\.au/s/article/[a-zA-Z0-9\-]+'

def scrape_askmq():
    articles = []
    skipped = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        visited = set()

        for category, url in category_pages.items():
            print(f"\n🔍 Scanning category: {category}")
            page.goto(url)
            page.wait_for_load_state("networkidle")
            time.sleep(3)

            html = page.content()
            links = re.findall(ARTICLE_LINK_PATTERN, html)
            unique_links = list(set(links) - visited)
            visited.update(unique_links)

            print(f"🔗 Found {len(unique_links)} unique article links in {category}")

            for link in unique_links:
                try:
                    page.goto(link)
                    page.wait_for_load_state("networkidle")
                    time.sleep(3)

                    # Extract title using the class structure you provided
                    title = page.evaluate("""() => {
                        const el = document.querySelector("dd.itemBody span.uiOutputText");
                        return el ? el.innerText : "";
                    }""")

                    # Extract full answer (innerText of div.slds-rich-text-editor__output)
                    answer = page.evaluate("""() => {
                        const el = document.querySelector("div.slds-rich-text-editor__output");
                        return el ? el.innerText : "";
                    }""")

                    if title and answer:
                        articles.append({
                            "category": category,
                            "title": title.strip(),
                            "answer": answer.strip(),
                            "url": link
                        })
                        print(f"✅ Scraped: {title.strip()}")
                    else:
                        print(f"⚠️ Missing title or answer for: {link}")
                        skipped.append(link)

                except Exception as e:
                    print(f"❌ Error scraping: {link} | {e}")
                    skipped.append(link)
                    continue

        browser.close()

    # Save results
    if articles:
        with open("askmq_articles_final.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["category", "title", "answer", "url"])
            writer.writeheader()
            writer.writerows(articles)
        print("\n✅ Done! Articles saved to askmq_articles_final.csv")

    if skipped:
        with open("skipped_links.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(skipped))
        print(f"⚠️ {len(skipped)} articles skipped. See skipped_links.txt")

if __name__ == "__main__":
    scrape_askmq()