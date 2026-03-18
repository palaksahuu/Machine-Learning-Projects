
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


with open("data.txt", "r", encoding="utf-8") as f:
    text_data = f.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
documents = text_splitter.split_text(text_data)


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.from_texts(documents, embedding_model)


vector_db.save_local("faiss_index")
print(" Embeddings Stored Successfully!")
