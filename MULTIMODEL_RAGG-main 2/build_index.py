import faiss
import numpy as np
import pickle

# Load your embedding vectors
with open("embeddings/your_vectors.pkl", "rb") as f:
    vectors = pickle.load(f)  

vectors = np.array(vectors).astype("float32")


index = faiss.IndexFlatL2(vectors.shape[1])  
index.add(vectors)
faiss.write_index(index, "embeddings/index.faiss")

print(" FAISS index built and saved successfully.")
