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
API_URL = "https://router.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

app = FastAPI(title="Faculty Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 🚀 NEW: KEEP-ALIVE MECHANISM ---
def keep_alive():
    """Pings the server every 10 minutes to prevent Render from sleeping."""
    while True:
        try:
            # Replace this with your actual Render URL
            requests.get("https://faculty-connect.onrender.com/")
            print("Pinged self to stay awake!")
        except Exception as e:
            print(f"Keep-alive ping failed: {e}")
        time.sleep(600) # 10 minutes

# Start the keep-alive thread automatically
threading.Thread(target=keep_alive, daemon=True).start()

# --- LOAD DATA ---
print("Loading Faculty Data...")
try:
    with open("faculty_data.pkl", "rb") as f:
        data = pickle.load(f)
        df = data['dataframe']
        embeddings = data['embeddings'] 
    print("✅ Data Loaded!")
except Exception as e:
    print(f"❌ Critical Error loading data: {e}")
    df = None

# HELPER: ASK HUGGING FACE WITH RETRY LOGIC
def query_hf_api(text):
    for i in range(3):  # Try 3 times
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=20)
            result = response.json()
            
            # If AI is still loading, wait and retry
            if isinstance(result, dict) and "estimated_time" in result:
                wait_time = result.get("estimated_time", 5)
                print(f"⏳ AI is warming up... waiting {wait_time}s")
                time.sleep(wait_time)
                continue
                
            return result
        except Exception as e:
            print(f"Retry {i+1} failed: {e}")
            time.sleep(2)
    return {"error": "AI Service Timeout. Please try again in a moment."}

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_faculty(request: SearchRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="Database not loaded")

    try:
        output = query_hf_api(request.query)
        
        if not isinstance(output, list):
            error_msg = output.get("error") if isinstance(output, dict) else "Unknown API Error"
            return {"results": [], "message": error_msg}

        query_vector = np.array(output)
        scores = np.dot(embeddings, query_vector.T).flatten()
        sorted_indices = scores.argsort()[::-1]

        results = []
        for idx in sorted_indices:
            current_score = float(scores[idx])
            # Set to 0.0 to ensure matches are found
            if current_score < 0.0: break 

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

        return {"results": results}

    except Exception as e:
        print(f"Server Crash: {e}")
        return {"results": [], "message": "The server encountered a math error. Try another query."}

@app.get("/")
def home():
    return {"message": "Faculty Search API is Live (Resilient & Awake Mode)!"}
