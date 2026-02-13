import sqlite3
import pandas as pd
import pickle
from sentence_transformers import SentenceTransformer

# 1. Load Data
conn = sqlite3.connect("faculty.db")
df = pd.read_sql_query("SELECT * FROM faculty", conn)
conn.close()

# 2. Prepare the "Context" (UPDATED)
# We now include Teaching and Publications so the AI "reads" them too.
df['combined_text'] = (
    "Name: " + df['Name'].fillna('') + ". " +
    "Specialization: " + df['Specialization'].fillna('') + ". " +
    "Research Interests: " + df['Research_Interests'].fillna('') + ". " +
    "Biography: " + df['Biography'].fillna('') + ". " +
    "Teaching: " + df['Teaching'].fillna('') + ". " +
    "Publications: " + df['Publications'].fillna('')
)

print(f"Loading {len(df)} faculty members with full details...")

# 3. Load Model & Generate Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(df['combined_text'].tolist(), show_progress_bar=True)

# 4. Save
with open("faculty_data.pkl", "wb") as f:
    pickle.dump({'dataframe': df, 'embeddings': embeddings}, f)

print("✅ Updated embeddings (with Publications & Teaching) saved!")