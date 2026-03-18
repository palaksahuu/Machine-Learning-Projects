import os
import json
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
# directory containing .txt file
DOCUMENTS_DIR = "data" 
# chunking configuration
CHUNK_SIZE = 500  
CHUNK_OVERLAP = 50  

# load .txt files
def load_documents_from_dir(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            loader = TextLoader(file_path, encoding='utf-8')
            loaded_docs = loader.load()
            for doc in loaded_docs:
                doc.metadata["source"] = filename
                documents.append(doc)
    return documents

# split each document into tokenbased chunk
def chunk_documents(documents, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunked_docs = splitter.split_documents(documents)

    # add chunk index  length metadata
    for i, doc in enumerate(chunked_docs):
        doc.metadata['chunk_index'] = i
        doc.metadata['chunk_length'] = len(doc.page_content)
    return chunked_docs

# save chunks to JSON for debugging
def save_chunks_to_json(chunks, file_path="chunks.json"):
    data = [
        {
            "content": chunk.page_content,
            "metadata": chunk.metadata
        }
        for chunk in chunks
    ]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Chunks saved to {file_path}")

# create FAISS vectorstore
def create_vectorstore(docs, persist_path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(persist_path)
    print(f"Vector store saved to '{persist_path}'")
    return vectorstore

# save chunks preview 
def preview_chunks(chunks, num=5):
    for i, chunk in enumerate(chunks[:num]):
        print(f"\nChunk #{i} | Source: {chunk.metadata['source']}")
        print(chunk.page_content[:300])

if __name__ == "__main__":
    print("Loading documents...")
    docs = load_documents_from_dir(DOCUMENTS_DIR)
    print(f"Loaded {len(docs)} documents")

    print("Chunking documents.")
    chunked_docs = chunk_documents(docs)
    print(f"Created {len(chunked_docs)} chunks")

   
    preview_chunks(chunked_docs)

    # save chunks to JSON
    save_chunks_to_json(chunked_docs)

    # create save FAISS vectorstore
    create_vectorstore(chunked_docs)
