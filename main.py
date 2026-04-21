import os
import time
import threading
import pickle
import numpy as np
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# --- CONFIGURATION ---
# Ensure HF_TOKEN is set in your Render environment variables
HF_TOKEN = os.environ.get("HF_TOKEN") 
API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

app = FastAPI(title="Connect2Faculty AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GLOBAL DATA ---
df = None
embeddings = None

def load_data():
    global df, embeddings
    try:
        # Load the pickle file generated during your preprocessing
        with open("faculty_data.pkl", "rb") as f:
            data = pickle.load(f)
            df = data['dataframe']
            # Convert to float32 and normalize immediately for cosine similarity
            raw_embeddings = np.array(data['embeddings']).astype('float32')
            norms = np.linalg.norm(raw_embeddings, axis=1, keepdims=True)
            embeddings = raw_embeddings / (norms + 1e-9)
        print(f"✅ Database Loaded: {len(df)} records.")
    except Exception as e:
        print(f"❌ DATABASE ERROR: {e}")

load_data()

# --- UTILITY: GET VECTOR FROM AI MODEL ---
def get_embedding(text):
    """Fetches vector from HF API with handling for nested lists and cold starts."""
    for i in range(3):  # Retry up to 3 times
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=20)
            result = response.json()
            
            # Handle API "Model is Loading" state
            if isinstance(result, dict) and "estimated_time" in result:
                wait = result.get("estimated_time", 10)
                print(f"⏳ Model loading... waiting {wait}s")
                time.sleep(wait)
                continue
            
            # Convert to numpy and flatten any nested structures (API often returns [[...]])
            vector = np.array(result).astype('float32')
            while len(vector.shape) > 1:
                vector = vector[0]

            if vector.size == 384:
                # Return normalized vector
                return vector / (np.linalg.norm(vector) + 1e-9)
            else:
                print(f"⚠️ Vector size mismatch: got {vector.size}, expected 384")
                return None
        except Exception as e:
            print(f"❌ HF API Attempt {i+1} failed: {e}")
            time.sleep(2)
    return None

# --- KEEP-ALIVE ---
def keep_alive():
    while True:
        try:
            # Change this to your actual Render URL
            requests.get("https://faculty-connect.onrender.com/", timeout=10)
        except:
            pass
        time.sleep(600) # Ping every 10 mins

threading.Thread(target=keep_alive, daemon=True).start()

# --- SEARCH ENDPOINT ---
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    if df is None or embeddings is None:
        raise HTTPException(status_code=500, detail="Database not initialized.")

    query_text = request.query.strip().lower()
    if not query_text:
        return {"results": []}

    final_results = []
    seen_names = set()

    # --- PHASE 1: EXACT/PARTIAL NAME MATCH ---
    # This fixes the "Abhishek" issue by checking text first
    name_matches = df[df['Name'].str.lower().str.contains(query_text, na=False)]
    
    for _, row in name_matches.iterrows():
        name = row.get("Name", "Unknown")
        final_results.append({
            "name": name,
            "specialization": row.get("Specialization", "N/A"),
            "image_url": row.get("Image_URL", ""),
            "profile_url": row.get("Profile_URL", ""),
            "score": 1.0,
            "match_type": "name"
        })
        seen_names.add(name)

    # --- PHASE 2: SEMANTIC SEARCH (TOPIC MATCH) ---
    # Only run if we haven't filled up the results with names
    if len(final_results) < 10:
        query_vec = get_embedding(query_text)
        
        if query_vec is not None:
            # Calculate Cosine Similarity via Dot Product (since vectors are normalized)
            scores = np.dot(embeddings, query_vec)
            top_indices = np.argsort(scores)[::-1]

            for idx in top_indices:
                row = df.iloc[idx]
                name = row.get("Name", "Unknown")
                
                # Filter results: avoid duplicates and low-relevance matches
                if name in seen_names or scores[idx] < 0.20:
                    continue
                
                final_results.append({
                    "name": name,
                    "specialization": row.get("Specialization", "N/A"),
                    "image_url": row.get("Image_URL", ""),
                    "profile_url": row.get("Profile_URL", ""),
                    "score": round(float(scores[idx]), 3),
                    "match_type": "semantic"
                })
                seen_names.add(name)
                if len(final_results) >= 15: break

    print(f"🔍 Query: '{query_text}' | Found: {len(final_results)}")
    return {"results": final_results}

@app.get("/")
def home():
    return {
        "status": "online", 
        "faculty_count": len(df) if df is not None else 0,
        "mode": "Hybrid (Name + Semantic)"
    }
