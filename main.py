from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pickle
import requests
import os
import time
import threading

# 🔒 SECURE: Must be set in Render Environment Variables
HF_TOKEN = os.environ.get("HF_TOKEN") 
API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
# Added User-Agent to prevent potential API blocks
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "User-Agent": "Connect2Faculty-App"
}

app = FastAPI(title="Connect2Faculty AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 🚀 KEEP-ALIVE ---
def keep_alive():
    while True:
        try:
            requests.get("https://faculty-connect.onrender.com/", timeout=10)
        except:
            pass
        time.sleep(600)

threading.Thread(target=keep_alive, daemon=True).start()

# --- LOAD DATA ---
print("🚀 Initializing Faculty Database...")
try:
    with open("faculty_data.pkl", "rb") as f:
        data = pickle.load(f)
        df = data['dataframe']
        embeddings = np.array(data['embeddings']) 
    print(f"✅ Data Loaded! Embeddings shape: {embeddings.shape}")
except Exception as e:
    print(f"❌ DATABASE ERROR: {e}")
    df = None
    embeddings = None

def query_hf_api(text):
    """Converts text to a 384-dimensional semantic vector"""
    for i in range(5): # Increased retries for stability
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=25)
            result = response.json()
            
            # Handle Cold-Starts or API errors
            if isinstance(result, dict) and "error" in result:
                err_msg = result["error"].lower()
                if "loading" in err_msg or "estimated_time" in result:
                    wait_time = result.get("estimated_time", 15)
                    print(f"⏳ Model loading... waiting {wait_time}s")
                    time.sleep(wait_time)
                    continue
                print(f"❌ HF API Error: {result['error']}")
                return None
            
            # Force Flattening to resolve 'Mismatch 1 vs 384'
            res = np.array(result).flatten()
            if res.size == 384:
                return res.tolist()
            else:
                print(f"❌ Dimension Mismatch! Received {res.size} dims")
                return None
                
        except Exception as e:
            print(f"Retry {i+1} failed: {e}")
            time.sleep(2)
    return None

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    if df is None or embeddings is None:
        raise HTTPException(status_code=500, detail="Database not loaded properly.")
    
    raw_vector = query_hf_api(request.query)
    
    if not raw_vector:
        return {"results": [], "message": "AI model is still warming up. Try again in 30s."}

    query_vec = np.array(raw_vector).flatten()
    
    if query_vec.shape[0] != 384:
        return {"results": [], "message": "AI model dimension mismatch."}

    # 3. Calculate Normalized Cosine Similarity
    try:
        # Prevent division by zero if vector is empty
        norm_q = query_vec / (np.linalg.norm(query_vec) + 1e-9)
        norm_e = embeddings / (np.linalg.norm(embeddings, axis=1, keepdims=True) + 1e-9)
        
        scores = np.dot(norm_e, norm_q)
        indices = np.argsort(scores)[::-1][:15]

        results = []
        for idx in indices:
            if scores[idx] < 0.01: continue 
            
            row = df.iloc[idx]
            results.append({
                "name": row.get("Name", "Unknown"),
                "specialization": row.get("Specialization", "N/A"),
                "image_url": row.get("Image_URL", ""),
                "profile_url": row.get("Profile_URL", ""),
                "score": float(scores[idx])
            })

        print(f"✅ Found {len(results)} matches for: {request.query}")
        return {"results": results}
    except Exception as e:
        print(f"❌ Math Error: {e}")
        return {"results": [], "message": "Error calculating similarity."}

@app.get("/")
def home():
    return {
        "message": "API is online!", 
        "status": "Ready", 
        "db_entries": len(df) if df is not None else 0
    }
