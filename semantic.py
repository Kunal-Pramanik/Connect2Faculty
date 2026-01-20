import pandas as pd
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer

# ---------- Helper: clean text ----------
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# ---------- Load data ----------
df = pd.read_csv("dau_faculty_clean.csv")

# ---------- Load model & FAISS index ----------
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("faculty_index.faiss")

# ---------- Semantic Search Function ----------
def search_faculty(query, top_k=5):
    query = clean_text(query)
    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding),
        top_k
    )

    results = df.iloc[indices[0]][
        ["Name", "Education", "Profile_URL"]
    ]

    return results

# ---------- TEST QUERY ----------
if __name__ == "__main__":
    query = "Find relevant faculty members even if specific phrases are not in their department title"
    results = search_faculty(query)
    print("\nSearch Results:\n")
    print(results)
