
import numpy as np
import pickle
import os

# Replace this with your real embedding generator
vectors = np.random.rand(100, 384).astype("float32")
os.makedirs("embeddings", exist_ok=True)

with open("embeddings/your_vectors.pkl", "wb") as f:
    pickle.dump(vectors, f)
