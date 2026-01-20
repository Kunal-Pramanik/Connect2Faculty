import pandas as pd
import re

df = pd.read_csv("dau_faculty.csv")
df.columns = df.columns.str.strip()

def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["Research Interests"].apply(clean_text)

# ✅ DROP EMPTY ROWS
df = df[df["clean_text"] != ""]

# Reset index
df = df.reset_index(drop=True)

df.to_csv("dau_faculty_clean.csv", index=False)

print("Remaining rows:", len(df))
