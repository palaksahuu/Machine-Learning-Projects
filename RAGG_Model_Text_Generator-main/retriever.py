import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

# load FAISS vectorstore and search
def retrieve_top_k(query, k=3, persist_path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Load saved vectorstore
    vectorstore = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)

    # perform similarity search
    results = vectorstore.similarity_search(query, k=k)

    # display top k results
    for i, doc in enumerate(results):
        print(f"\n Result #{i + 1}")
        print("Content:", doc.page_content[:300], "...")
        print("Metadata:", doc.metadata)

    return results

if __name__ == "__main__":
    # example
    user_query = input("Enter your query: ")
    retrieve_top_k(user_query, k=3)
