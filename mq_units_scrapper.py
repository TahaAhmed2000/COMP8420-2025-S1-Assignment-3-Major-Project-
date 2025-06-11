# import requests
# from bs4 import BeautifulSoup
# import csv
# import re
# import time
# from urllib.parse import urljoin

# BASE_URL = "https://unitguides.mq.edu.au"
# UNITS_PAGE = f"{BASE_URL}/units"

# def get_faculty_department_links():
#     response = requests.get(UNITS_PAGE)
#     soup = BeautifulSoup(response.text, "html.parser")
#     links = []

#     for a_tag in soup.find_all("a", href=True):
#         href = a_tag["href"]
#         if "/units/show_year/2025/" in href:
#             full_url = urljoin(BASE_URL, href)
#             links.append(full_url)

#     return links

# def get_unit_guide_links(faculty_url):
#     response = requests.get(faculty_url)
#     soup = BeautifulSoup(response.text, "html.parser")
#     links = []

#     for a_tag in soup.find_all("a", href=True):
#         href = a_tag["href"]
#         if "/unit_offerings/" in href and "/unit_guide" in href:
#             full_url = urljoin(BASE_URL, href)
#             links.append(full_url)

#     return links

# def scrape_unit_guide(unit_url):
#     response = requests.get(unit_url)
#     soup = BeautifulSoup(response.text, "html.parser")

#     # Extract unit code and title
#     h1_tag = soup.find("h1")
#     if h1_tag:
#         title_text = h1_tag.get_text(strip=True)
#         match = re.match(r"([A-Z]{4}\d{4})\s*–\s*(.+)", title_text)
#         if match:
#             unit_code = match.group(1)
#             unit_title = match.group(2)
#         else:
#             unit_code = ""
#             unit_title = title_text
#     else:
#         unit_code = ""
#         unit_title = ""

#     # Extract content
#     content_div = soup.find("div", class_="unit-guide")
#     content = content_div.get_text(separator="\n", strip=True) if content_div else ""

#     return {
#         "unit_code": unit_code,
#         "title": unit_title,
#         "url": unit_url,
#         "content": content
#     }

# def main():
#     faculty_links = get_faculty_department_links()
#     all_unit_guides = []

#     for faculty_url in faculty_links:
#         print(f"Processing faculty/department page: {faculty_url}")
#         unit_links = get_unit_guide_links(faculty_url)
#         for unit_url in unit_links:
#             print(f"Scraping unit guide: {unit_url}")
#             unit_data = scrape_unit_guide(unit_url)
#             all_unit_guides.append(unit_data)
#             time.sleep(1)  # Be polite and avoid overwhelming the server

#     # Save to CSV
#     with open("mq_unit_guides_2025.csv", "w", newline="", encoding="utf-8") as csvfile:
#         fieldnames = ["unit_code", "title", "url", "content"]
#         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#         writer.writeheader()
#         for unit in all_unit_guides:
#             writer.writerow(unit)

#     print("Scraping completed. Data saved to mq_unit_guides_2025.csv.")

# if __name__ == "__main__":
#     main()

import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin

BASE_URL = "https://unitguides.mq.edu.au"
UNITS_PAGE = f"{BASE_URL}/units"

def get_faculty_department_links():
    response = requests.get(UNITS_PAGE)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "/units/show_year/2025/" in href:
            full_url = urljoin(BASE_URL, href.split("?")[0])  # remove any existing ?page=
            links.append(full_url)

    return sorted(set(links))

def get_unit_guide_links_with_pagination(department_url):
    page = 1
    collected_links = []

    while True:
        url = f"{department_url}?page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.text, "html.parser")
        new_links = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if "/unit_offerings/" in href and "/unit_guide" in href:
                full_url = urljoin(BASE_URL, href)
                if full_url not in collected_links:
                    new_links.append(full_url)

        if not new_links:
            break

        collected_links.extend(new_links)
        page += 1
        time.sleep(0.5)  # polite crawling

    return collected_links

def main():
    faculty_links = get_faculty_department_links()
    all_unit_links = []

    for dept_url in faculty_links:
        print(f"\n📂 Department page: {dept_url}")
        unit_links = get_unit_guide_links_with_pagination(dept_url)
        print(f"🔗 Found {len(unit_links)} unit guide links.")
        for link in unit_links:
            all_unit_links.append({"url": link})

    # Save just the URLs to CSV
    with open("mq_unit_guide_links_2025.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["url"])
        writer.writeheader()
        writer.writerows(all_unit_links)

    print(f"\n✅ Total unit links collected: {len(all_unit_links)}")
    print("🔽 Saved to mq_unit_guide_links_2025.csv")

if __name__ == "__main__":
    main()