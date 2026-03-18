
import os
import json
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

# xample text chunks
texts = [
    "Sachin Tendulkar is a legendary Indian cricketer.",
    "Virat Kohli is known for his aggressive batting style.",
    "MS Dhoni led India to victory in the 2011 World Cup.",
]

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# enerate embeddings
embeddings = model.encode(texts).astype("float32")

# ave vectors
os.makedirs("embeddings", exist_ok=True)
with open("embeddings/your_vectors.pkl", "wb") as f:
    pickle.dump(embeddings, f)

# save metadata
metadata = [{"text": text} for text in texts]
with open("embeddings/metadata.json", "w") as f:
    json.dump(metadata, f, indent=2)

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)
faiss.write_index(index, "embeddings/index.faiss")
