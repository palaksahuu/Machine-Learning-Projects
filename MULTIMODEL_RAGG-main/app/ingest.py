
from sentence_transformers import SentenceTransformer
from PIL import Image
import clip
import torch
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
text_encoder = SentenceTransformer('all-MiniLM-L6-v2')
clip_model, preprocess = clip.load("ViT-B/32", device=device)

def embed_text(text):
    return text_encoder.encode([text])[0]

def embed_image(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        return clip_model.encode_image(image).cpu().numpy()[0]
