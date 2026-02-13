import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Load resources once
print("Loading search engine...")
model = SentenceTransformer('all-MiniLM-L6-v2')

with open("faculty_data.pkl", "rb") as f:
    data = pickle.load(f)
    df = data['dataframe']
    faculty_embeddings = data['embeddings']

def search_faculty(query, top_k=5):
    # 1. Vectorize query
    query_embedding = model.encode([query])

    # 2. Calculate Similarity
    # Using cosine similarity (dot product of normalized vectors)
    similarities = np.dot(faculty_embeddings, query_embedding.T).flatten()

    # 3. Get Top K indices
    top_indices = similarities.argsort()[-top_k:][::-1]

    # 4. Fetch results (UPDATED to include new fields)
    results = []
    for idx in top_indices:
        results.append({
            "name": df.iloc[idx]['Name'],
            "specialization": df.iloc[idx]['Specialization'],
            "image_url": df.iloc[idx]['Image_URL'],
            "profile_url": df.iloc[idx]['Profile_URL'],
            
            # --- NEW FIELDS ---
            "teaching": df.iloc[idx]['Teaching'],
            "publications": df.iloc[idx]['Publications'],
            
            "score": float(similarities[idx])
        })
    
    return results

# --- TEST IT OUT ---
if __name__ == "__main__":
    # Try a query that targets the new fields
    user_query = "Who teaches machine learning and has published on neural networks?"
    
    matches = search_faculty(user_query)

    print(f"\nSearch Results for: '{user_query}'\n" + "-"*40)
    for faculty in matches:
        print(f"Name: {faculty['name']}")
        # Print a snippet of teaching to verify it worked
        print(f"Teaches: {str(faculty['teaching'])[:50]}...") 
        print(f"Link: {faculty['profile_url']}")
        print("-" * 20)