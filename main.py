from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import requests
import os
import time
import threading

# 🔒 SECURE WAY: Read from Environment Variable
HF_TOKEN = os.environ.get("HF_TOKEN") 
API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

app = FastAPI(title="Faculty Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 🚀 KEEP-ALIVE MECHANISM ---
def keep_alive():
    while True:
        try:
            requests.get("https://faculty-connect.onrender.com/", timeout=10)
            print("Pinged self to stay awake!")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(600)

threading.Thread(target=keep_alive, daemon=True).start()

# --- LOAD DATA ---
print("Loading Faculty Data...")
try:
    with open("faculty_data.pkl", "rb") as f:
        data = pickle.load(f)
        df = data['dataframe']
        embeddings = np.array(data['embeddings']) # Ensure it's a numpy array
    print(f"✅ Data Loaded! Embeddings Shape: {embeddings.shape}")
except Exception as e:
    print(f"❌ Critical Error loading data: {e}")
    df = None

# --- HELPER: ASK HUGGING FACE ---
def query_hf_api(text):
    for i in range(3):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=20)
            result = response.json()
            
            if isinstance(result, dict) and "estimated_time" in result:
                wait_time = result.get("estimated_time", 5)
                print(f"⏳ AI warming up... waiting {wait_time}s")
                time.sleep(wait_time)
                continue
                
            if isinstance(result, list) and len(result) > 0:
                # Extract first element if nested
                vector = result[0] if isinstance(result[0], list) else result
                return vector
                
            return result
        except Exception as e:
            print(f"Retry {i+1} failed: {e}")
            time.sleep(2)
    return {"error": "AI Service Timeout."}

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_faculty(request: SearchRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="Database not loaded")

    try:
        # 1. Get embedding
        output = query_hf_api(request.query)
        if not isinstance(output, list):
            return {"results": [], "message": str(output.get("error", "API Error"))}

        # 2. Prepare Vector & Normalize
        query_vector = np.array(output)
        query_vector = query_vector / np.linalg.norm(query_vector) # ✨ Normalize for better matching

        # 3. Calculate Scores (Dot Product)
        # Check dimensions first
        if query_vector.shape[0] != embeddings.shape[1]:
            print(f"Dimension mismatch! Query: {query_vector.shape[0]}, DB: {embeddings.shape[1]}")
            return {"results": [], "message": "Search model version mismatch."}

        scores = np.dot(embeddings, query_vector)
        sorted_indices = np.argsort(scores)[::-1]

        results = []
        for idx in sorted_indices[:10]: # Limit to top 10 for speed
            current_score = float(scores[idx])
            
            # Use a very low threshold during testing
            if current_score < -1.0: break 

            faculty_data = df.iloc[idx]
            results.append({
                "name": faculty_data.get("Name", "Unknown"),
                "specialization": faculty_data.get("Specialization", "N/A"),
                "image_url": faculty_data.get("Image_URL", ""),
                "profile_url": faculty_data.get("Profile_URL", ""),
                "teaching": faculty_data.get("Teaching", "N/A"),
                "publications": faculty_data.get("Publications", "N/A"),
                "score": current_score
            })

        print(f"✅ Success: Found {len(results)} matches for '{request.query}'")
        return {"results": results}

    except Exception as e:
        print(f"❌ Server Error: {e}")
        return {"results": [], "message": f"Calculation error: {str(e)}"}

@app.get("/")
def home():
    return {"message": "FacultyConnect API is Live and Awake!"}
