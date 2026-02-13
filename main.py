from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import os

# 1. SETUP APP
app = FastAPI(title="Faculty Finder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. GLOBAL VARIABLES (Start as None)
model = None
df = None
embeddings = None

# 3. HELPER: LOAD MODEL ONLY WHEN NEEDED
def load_resources():
    global model, df, embeddings
    if model is None:
        print("⏳ Loading AI Model & Data... (First run only)")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        with open("faculty_data.pkl", "rb") as f:
            data = pickle.load(f)
            df = data['dataframe']
            embeddings = data['embeddings']
        print("✅ Model Loaded!")

# 4. SEARCH ENDPOINT
class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search_faculty(request: SearchRequest):
    # Load the model now (if not already loaded)
    load_resources()
    
    try:
        query_vector = model.encode([request.query])
        scores = np.dot(embeddings, query_vector.T).flatten()
        sorted_indices = scores.argsort()[::-1]

        results = []
        for idx in sorted_indices:
            current_score = float(scores[idx])
            if current_score < 0.15: break 

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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Faculty Search API is Live!"}
