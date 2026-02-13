from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import requests
import os

# ---------------------------------------------------------
# 🔒 SECURE WAY: Read from Environment Variable
# ---------------------------------------------------------
HF_TOKEN = os.environ.get("HF_TOKEN") 

API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# 1. SETUP APP
app = FastAPI(title="Faculty Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. LOAD DATA (Lightweight!)
print("Loading Faculty Data...")
try:
    with open("faculty_data.pkl", "rb") as f:
        data = pickle.load(f)
        df = data['dataframe']
        embeddings = data['embeddings'] 
    print("✅ Data Loaded!")
except FileNotFoundError:
    print("⚠️ Warning: faculty_data.pkl not found. Make sure it's in the same folder.")
    df = None
    embeddings = None

# 3. HELPER: ASK HUGGING FACE FOR EMBEDDINGS
def query_hf_api(text):
    if not HF_TOKEN:
        return {"error": "Missing HF_TOKEN. Please set it in Render Environment Variables."}
    response = requests.post(API_URL, headers=headers, json={"inputs": text})
    return response.json()

# 4. SEARCH ENDPOINT
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_faculty(request: SearchRequest):
    if df is None:
        raise HTTPException(status_code=500, detail="Server Error: Database file missing")

    try:
        # A. Ask the Cloud API to convert query to numbers
        output = query_hf_api(request.query)
        
        # Error handling if API is waking up
        if isinstance(output, dict) and "error" in output:
            print(f"HuggingFace Error: {output}")
            return {"results": [], "message": "AI is warming up or Token is invalid. Try again in 10s"}
            
        # B. Convert list to numpy array
        if isinstance(output, list):
            query_vector = np.array(output)
        else:
            return {"results": [], "message": "API Error: Unexpected response format"}

        # C. Calculate Similarity
        scores = np.dot(embeddings, query_vector.T).flatten()
        sorted_indices = scores.argsort()[::-1]

        # D. Get Results
        results = []
        for idx in sorted_indices:
            current_score = float(scores[idx])
            
            # --- FIX IS HERE: Lowered from 0.15 to 0.0 ---
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
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Faculty Search API is Live (Secure Mode)!"}
