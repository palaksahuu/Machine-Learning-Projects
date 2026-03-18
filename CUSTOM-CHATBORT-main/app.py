
from flask import Flask, request, jsonify
from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings


app = Flask(__name__)
@app.route('/')
def home():
    return "Custom Chatbot API is Running!"


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)

@app.route('/chat', methods=['POST'])
def chat():
    user_query = request.json.get("query")
    
    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    results = vector_db.similarity_search(user_query, k=3)
    
    if not results:
        return jsonify({"response": "No relevant results found."})
    
    response_text = "\n".join([res.page_content for res in results])
    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)
