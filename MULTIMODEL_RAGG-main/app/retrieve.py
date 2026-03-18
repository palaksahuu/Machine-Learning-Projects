
import faiss
import numpy as np
import json


index = faiss.read_index("embeddings/index.faiss")
with open("embeddings/metadata.json", "r") as f:
    metadata = json.load(f)

def search(query_embedding, top_k=3):
    D, I = index.search(np.array([query_embedding]), top_k)
    return [metadata[i] for i in I[0]]
