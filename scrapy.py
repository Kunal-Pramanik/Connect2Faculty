import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE = "https://www.daiict.ac.in"
URLS = [
    f"{BASE}/faculty",
    f"{BASE}/adjunct-faculty",
    f"{BASE}/adjunct-faculty-international",
    f"{BASE}/distinguished-professor",
    f"{BASE}/professor-practice"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

faculty_list = []


# -------------------------
# Helper functions
# -------------------------
def get_text(parent, cls):
    tag = parent.find(class_=cls)
    return tag.get_text(strip=True) if tag else "N/A"


def get_profile_link(card):
    a = card.find("a", href=True)
    if not a:
        return "N/A", "N/A"
    link = a["href"]
    if not link.startswith("http"):
        link = BASE + link
    return a.get_text(strip=True), link


# -------------------------
# PROFILE PAGE SCRAPER
# -------------------------
def scrape_profile(url):
    data = {
        "Biography": "N/A",
        "Research Interests": "N/A",
        "Teaching": "N/A",
        "Publications": "N/A"
    }

    try:
        soup = BeautifulSoup(
            requests.get(url, headers=HEADERS, timeout=15).text,
            "html.parser"
        )
    except:
        return data

    # -------------------------
    # Biography
    # -------------------------
    about = soup.select_one("div.about")
    if about:
        data["Biography"] = " ".join(
            p.get_text(strip=True) for p in about.find_all("p")
        )

    # -------------------------
    # Research Interests / Specialization
    
    spec_block = soup.select_one("div.work-exp.margin-bottom-20 p")
    if spec_block and spec_block.get_text(strip=True):
        data["Research Interests"] = spec_block.get_text(strip=True)

   
    # Teaching
 
    teaching_items = [
        li.get_text(strip=True)
        for li in soup.select("div.work-exp ul li")
        if li.get_text(strip=True)
    ]
    if teaching_items:
        data["Teaching"] = " | ".join(teaching_items)

 
    # Publications
 
    pub_block = soup.select_one("div.education.overflowContent")
    if pub_block:
        pubs = [
            li.get_text(strip=True)
            for li in pub_block.find_all("li")
            if li.get_text(strip=True)
        ]
        if pubs:
            data["Publications"] = " | ".join(pubs)

    return data


# -------------------------
# MAIN SCRAPING LOOP
# -------------------------
for url in URLS:
    print(f"\n🔹 Fetching: {url}")
    soup = BeautifulSoup(
        requests.get(url, headers=HEADERS).text,
        "html.parser"
    )

    cards = soup.select("div.facultyDetails, div.views-row, article.node")
    print("Found faculty:", len(cards))

    for card in cards:
        name, profile_url = get_profile_link(card)

        profile_data = scrape_profile(profile_url) if profile_url != "N/A" else {
            "Biography": "N/A",
            "Research Interests": "N/A",
            "Teaching": "N/A",
            "Publications": "N/A"
        }

        faculty_list.append({
            "Name": name,
            "Profile URL": profile_url,
            "Qualification": get_text(card, "facultyEducation"),
            "Phone": get_text(card, "facultyNumber"),
            "Address": get_text(card, "facultyAddress"),
            "Email": get_text(card, "facultyemail"),
            "Specialization": get_text(card, "areaSpecialization"),
            "Image URL": card.find("img")["src"] if card.find("img") else "N/A",
            "Biography": profile_data["Biography"],
            "Research Interests": profile_data["Research Interests"],
            "Teaching": profile_data["Teaching"],
            "Publications": profile_data["Publications"]
        })

        time.sleep(1)


# -------------------------
# SAVE CSV
# -------------------------
df = pd.DataFrame(faculty_list)

# Safety cleanup
df[["Research Interests", "Teaching"]] = df[
    ["Research Interests", "Teaching"]
].fillna("N/A")

df.to_csv("daiict_full_faculty_data.csv", index=False)

print("\n✅ DONE!")
print("Total faculty scraped:", len(df))
