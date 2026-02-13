from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import pickle
import os

# -------------------------
# 1. SETUP APP & CORS
# -------------------------
app = FastAPI(title="Faculty Finder API", description="Semantic Search Engine for Faculty")

# Enable CORS so your frontend (localhost:3000 or public URL) can talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# 2. GLOBAL VARIABLES (Load Once)
# -------------------------
print("⏳ Loading AI Model & Data... (This takes a few seconds)")

# Load the Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load the Data
with open("faculty_data.pkl", "rb") as f:
    data = pickle.load(f)
    df = data['dataframe']
    embeddings = data['embeddings']

print("✅ Server Ready! Model & Data Loaded.")

# -------------------------
# 3. DATA MODELS
# -------------------------
class SearchRequest(BaseModel):
    query: str
    # Removed top_k from here since we want all matches

@app.post("/search")
async def search_faculty(request: SearchRequest):
    try:
        # A. Vectorize query
        query_vector = model.encode([request.query])

        # B. Calculate Similarity
        scores = np.dot(embeddings, query_vector.T).flatten()

        # C. Sort scores (Highest first) - NO SLICING [:top_k]
        sorted_indices = scores.argsort()[::-1]

        # D. Build Response
        results = []
        for idx in sorted_indices:
            current_score = float(scores[idx])
            
            # Optional: Filter out completely irrelevant matches (noise)
            # You can lower this to 0.0 if you want absolutely everyone
            if current_score < 0.15: 
                break 

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
# -------------------------
# 5. HEALTH CHECK
# -------------------------
@app.get("/")
def home():
    return {"message": "Faculty Search API is running! Go to /docs to test."}