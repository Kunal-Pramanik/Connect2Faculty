import numpy as np 
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

#load clean data
df=pd.read_csv("dau_faculty_clean.csv")

#load sentence BERT model
model = SentenceTransformer("all-MiniLM-L6-v2")

#convert text to embedding
embeddings = model.encode(
    df["clean_text"].astype(str).tolist(),
    show_progress_bar=True
)

#build faiss index
dimension=embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print("Total faculty indexed:", index.ntotal)

#save index
faiss.write_index(index, "faculty_index.faiss")