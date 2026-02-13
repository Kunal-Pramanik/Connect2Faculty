import pandas as pd
import re

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("daiict_faculty_data.csv")
df.columns = df.columns.str.strip()

# -------------------------
# TEXT CLEANING FUNCTION
# -------------------------
def clean_text(text):
    if pd.isna(text) or text == "N/A":
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# -------------------------
# CLEAN RESEARCH INTERESTS
# -------------------------
df["Research Interests"] = df["Research Interests"].apply(clean_text)

# -------------------------
# CLEAN EMAILS
# -------------------------
df["Email"] = (
    df["Email"]
    .astype(str)
    .str.replace("[at]", "@", regex=False)
    .str.replace("[dot]", ".", regex=False)
)

# -------------------------
# DROP EMPTY RESEARCH INTERESTS
# -------------------------
df = df[df["Research Interests"] != ""]

# -------------------------
# RESET INDEX
# -------------------------
df = df.reset_index(drop=True)

# -------------------------
# ADD FACULTY ID
# -------------------------
df.insert(
    0,
    "faculty_id",
    [f"F-{str(i + 1).zfill(3)}" for i in range(len(df))]
)

# -------------------------
# SAVE CLEAN FILE
# -------------------------
df.to_csv("dau_faculty.csv", index=False)

print("Remaining rows:", len(df))
