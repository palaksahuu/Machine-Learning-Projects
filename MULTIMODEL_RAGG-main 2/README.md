## Multimodal Retrieval Augmented Generation Pipeline

## 1. Project cover

-Accepts text and image queries.

-Retrieves semantically similar text and images using embedding search.

-Passes retrieved content to a multimodal LLM (LLaVA) for response generation.

-Does not use OCR for image understanding : instead, it directly processes images using CLIP & LLaVA.

Project Structure
bash
Copy code

## 2. Project Structure

├── app/
│   ├── ingest.py              
│   ├── retrieve.py         
│   └── generate.py            
├── main.py                    
├── build_index.py             
├── generate_embedding.py     
├── generate_vector.py       
├── embeddings/
│   ├── your_vectors.pkl      
│   ├── metadata.json          
│   └── index.faiss           
└── README.md  

## 3. Setup & Installation

-create a venv enviornment and activate the enviornment

## 4. Install Dependencies

pip install -r requirements.txt

sentence-transformers
faiss-cpu
transformers
torchvision
openai
pillow
fastapi
uvicorn
python-multipart
numpy
faiss
pillow
torch
torchvision
ftfy
regex
fastapi
torch
llava @ git+https://github.com/haotian-liu/LLaVA.git

## 5. Clone the repository

git clone https://github.com/yourusername/multimodal-rag.git
cd multimodal-rag

## Download LLaVA Weights

model_path = "liuhaotian/llava-v1.5-13b"


## 6. Running the Application


run this commond : uvicorn main:app --reload


## Workflow Summary


-Query Ingestion:
Accepts either a text string or an image file.

-Embedding Generation:

T-ext: SentenceTransformer

-Image: CLIP ViT-B/32

-Semantic Retrieval:

-Uses FAISS to retrieve the top-k relevant text/image embeddings from a shared vector space.

-Multimodal Generation:
Retrieved context (text + image) is passed to LLaVA.

-LLaVA generates a coherent answer without using OCR