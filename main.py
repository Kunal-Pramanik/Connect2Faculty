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

# --- DATABASE LOADING ---
df = None
embeddings = None

def load_data():
    global df, embeddings
    try:
        with open("faculty_data.pkl", "rb") as f:
            data = pickle.load(f)
            df = data['dataframe']
            embeddings = np.array(data['embeddings'])
            # Pre-normalize embeddings for faster cosine similarity calculation
            norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
            embeddings = embeddings / (norms + 1e-9)
        print(f"✅ Database Loaded: {len(df)} records.")
    except Exception as e:
        print(f"❌ Critical Load Error: {e}")

load_data()

# --- UTILITIES ---
def get_embedding(text):
    """Fetches vector from HF API with retry logic for cold starts."""
    for _ in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=20)
            result = response.json()
            
            if isinstance(result, dict) and "estimated_time" in result:
                time.sleep(result["estimated_time"])
                continue
                
            vector = np.array(result).flatten()
            if vector.size == 384:
                return vector / (np.linalg.norm(vector) + 1e-9)
        except:
            time.sleep(1)
    return None

def keep_alive():
    while True:
        try:
            # Replace with your actual deployment URL
            requests.get("https://faculty-connect.onrender.com/", timeout=10)
        except:
            pass
        time.sleep(600)

threading.Thread(target=keep_alive, daemon=True).start()

# --- API ENDPOINTS ---
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    if df is None or embeddings is None:
        raise HTTPException(status_code=500, detail="Database not initialized.")

    user_query = request.query.strip().lower()
    final_results = []
    seen_names = set()

    # 1. PRIORITY MATCH: Name-based Search (Fixes the 'Abhishek' issue)
    # We look for the query string inside the 'Name' column
    name_matches = df[df['Name'].str.lower().str.contains(user_query, na=False)]
    
    for _, row in name_matches.iterrows():
        name = row.get("Name", "Unknown")
        final_results.append({
            "name": name,
            "specialization": row.get("Specialization", "N/A"),
            "image_url": row.get("Image_URL", ""),
            "profile_url": row.get("Profile_URL", ""),
            "score": 1.0, # Exact/Partial name matches get top priority
            "match_type": "name"
        })
        seen_names.add(name)

    # 2. SEMANTIC MATCH: Topic-based Search (Only if we need more results)
    if len(final_results) < 10:
        query_vec = get_embedding(user_query)
        
        if query_vec is not None:
            # Calculate cosine similarities
            scores = np.dot(embeddings, query_vec)
            top_indices = np.argsort(scores)[::-1]

            for idx in top_indices:
                row = df.iloc[idx]
                name = row.get("Name", "Unknown")
                
                # Skip if already added via name match or if score is too low
                if name in seen_names or scores[idx] < 0.25:
                    continue
                
                final_results.append({
                    "name": name,
                    "specialization": row.get("Specialization", "N/A"),
                    "image_url": row.get("Image_URL", ""),
                    "profile_url": row.get("Profile_URL", ""),
                    "score": float(scores[idx]),
                    "match_type": "semantic"
                })
                seen_names.add(name)
                if len(final_results) >= 15: break

    return {"results": final_results[:15]}

@app.get("/")
def home():
    return {"status": "online", "count": len(df) if df is not None else 0}
