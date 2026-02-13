import pandas as pd
import numpy as np
import pickle
import requests
import sqlite3
import os
import time  

# 1. Setup 
# Replace the string below with your actual token from: https://huggingface.co/settings/tokens
HF_TOKEN = "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" 
API_URL = "https://router.huggingface.co/hf-inference/models/sentence-transformers/all-MiniLM-L6-v2/pipeline/feature-extraction"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def get_embedding(text):
    for i in range(5):
        try:
            response = requests.post(API_URL, headers=headers, json={"inputs": text}, timeout=30)
            result = response.json()
            
            if isinstance(result, dict):
                # Handle model loading
                if "estimated_time" in result:
                    wait_time = result.get("estimated_time", 10)
                    print(f"⏳ AI warming up... waiting {wait_time}s")
                    time.sleep(wait_time)
                    continue
                # Handle Auth or API errors
                if "error" in result:
                    print(f"❌ API Error: {result['error']}")
                    if "Invalid username or password" in result['error']:
                        print("👉 Please check your HF_TOKEN at https://huggingface.co/settings/tokens")
                    time.sleep(5)
                    continue
            
            if isinstance(result, list) and len(result) > 0:
                return result[0] if isinstance(result[0], list) else result
                
        except Exception as e:
            print(f"Attempt {i+1} failed: {e}")
            time.sleep(2)
            
    raise Exception("Failed to get embedding after multiple retries.")

# 2. Load Data
try:
    conn = sqlite3.connect("faculty.db")
    df = pd.read_sql_query("SELECT * FROM faculty", conn)
    conn.close()
    print(f"✅ Loaded {len(df)} faculty members.")
except Exception as e:
    print(f"❌ DB Error: {e}")
    exit()

# 3. Generate 
print("🔄 Syncing database with Hugging Face API...")
all_embeddings = []
for i, row in df.iterrows():
    # Combining text for better search context
    text = f"{row.get('Name', '')} {row.get('Specialization', '')} {row.get('Research_Interests', '')}"
    all_embeddings.append(get_embedding(text))
    if i % 5 == 0: 
        print(f"Progress: {i}/{len(df)}")

# 4. Save
embeddings_array = np.array(all_embeddings).astype('float32')
with open("faculty_data.pkl", "wb") as f:
    pickle.dump({'dataframe': df, 'embeddings': embeddings_array}, f)

print(f"✅ SUCCESS! Generated {embeddings_array.shape} embeddings.")