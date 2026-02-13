import pandas as pd
import sqlite3



conn = sqlite3.connect("faculty.db")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    faculty_id TEXT PRIMARY KEY,
    Name TEXT,
    Profile_URL TEXT,
    Qualification TEXT,
    Phone TEXT,
    Address TEXT,
    Email TEXT,
    Specialization TEXT,
    Image_URL TEXT,
    Biography TEXT,
    Research_Interests TEXT,
    Teaching TEXT,
    Publications TEXT
)
""")



df = pd.read_csv("dau_faculty.csv")

# Rename columns to match SQL 
df = df.rename(columns={
    "Profile URL": "Profile_URL",
    "Image URL": "Image_URL",
    "Research Interests": "Research_Interests"
})


# INSERT DATA

df.to_sql(
    "faculty",
    conn,
    if_exists="append",
    index=False
)

conn.commit()
conn.close()

print(" Data pushed successfully into SQLite")
