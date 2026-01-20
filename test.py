import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.daiict.ac.in/faculty"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

faculty_data = []

# Each faculty card
faculty_cards = soup.select("div.facultyInformation ul li")

for card in faculty_cards:
    # Name + Profile URL
    name_tag = card.select_one("h3 a")
    name = name_tag.get_text(strip=True) if name_tag else ""
    profile_url = name_tag["href"] if name_tag else ""

    # Education
    edu_tag = card.select_one("div.facultyEducation")
    education = edu_tag.get_text(strip=True) if edu_tag else ""

    # Research / Bio text
    bio_tag = card.select_one("div.areaSpecialization p")
    bio_text = bio_tag.get_text(strip=True) if bio_tag else ""

    faculty_data.append({
        "Name": name,
        "Education": education,
        "Bio_Text": bio_text,
        "Profile_URL": profile_url
    })

# Create DataFrame
df = pd.DataFrame(faculty_data)

# Save
df.to_csv("dau_faculty1.csv", index=False)

print(df.head())
