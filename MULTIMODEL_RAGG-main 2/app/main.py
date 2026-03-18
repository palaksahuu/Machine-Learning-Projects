from fastapi import FastAPI, UploadFile, Form
from app.ingest import embed_text, embed_image
from app.retrieve import search
from app.generate import generate_answer
import shutil
import os

app = FastAPI()

@app.post("/query")
async def multimodal_query(query: str = Form(None), file: UploadFile = None):
    tmp_img_path = None

    if file:
        tmp_img_path = f"temp_{file.filename}"
        with open(tmp_img_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        embedding = embed_image(tmp_img_path)
    else:
        embedding = embed_text(query)

    results = search(embedding)
    retrieved_texts = [r["text"] for r in results if r["type"] == "text"]
    retrieved_images = [r["path"] for r in results if r["type"] == "image"]

    context = "\n".join(retrieved_texts)
    final_prompt = f"User Query: {query}\nContext: {context}"
    answer = generate_answer(final_prompt, retrieved_images)

    if tmp_img_path and os.path.exists(tmp_img_path):
        os.remove(tmp_img_path)

    return {"answer": answer}
