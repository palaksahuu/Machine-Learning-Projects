#  RAG Powered Knowledge Assistant

This project implements a simple yet powerful Knowledge Assistant using Retrieval Augmented Generation (RAG) , LLMs, and a basic Agentic Workflow. It uses open-source tools like LangChain, FAISS, Hugging Face Transformers, and Streamlit.

## Project Features

- Retrieves relevant information from a small document collection  
- Uses an LLM to generate natural-language answers  
- Routes queries using basic agent logic:
- Routes to a tool if the query includes calculate  or define.
- Otherwise, runs the RAG → LLM pipeline
- Displays agent decisions, retrieved contexts, and final answers in an interactive UI

---

##  File Structure

RAGG/
├── rag_chain.py         
├── data/ 
   |- airpods_manual.txt  
   |- copilot_blog.txt
   |- openai_faq.txt
   |- remote_work_policy.txt
   |- tesla_model3_specs.txt

├── faiss_index       
├── scripts
   |- chunking.py   

├── app.py      
├── rag_chain.py         
├── requirements.txt
└── README.md



##  Setup enviornment

## 1. Create a python enviorments

# Create a virtual environment named 'venv'
python3 -m venv venv

# Activate the environment
source venv/bin/activate

## 2. Install dependencies:

pip install -r requirements.txt


## 3. Run Python files follow 

1 Run the chunking + vector store builder:

python chunking.py

2 Run the retriever.py:

python retriever.py

3 Run the rag_chain.py:

python rag_chain.py

4. Launch the Streamlit UI:

streamlit run app.py 
(This command launches the Streamlit web interface for the project, allowing users to enter queries and receive answers from the RAG-powered multi-agent assistant)

# Example Queries:
define AI

what is GitHub Copilot?

how to connect AirPods?

what is remote work policy?

-> How It Works
➤ RAG Pipeline
Retrieves top-3 most relevant chunks from the vector store using FAISS and passes them as context to a HuggingFace LLM (GPT-2).

➤ Agentic Workflow
Routes the user query based on its content:

If calculate or define → uses built-in tool function

Otherwise → uses RAG + LLM to generate the answer

➤ Streamlit UI
Provides an interactive interface to:

Input questions

See which logic branch was chosen

View retrieved context and final answer

- Sample Documents Used
openai_faq.txt
remote_work_policy.txt
airpods_manual.txt
copilot_blog.txt
tesla_model3_specs.txt

-Tech Stack
LangChain
FAISS 
Hugging Face Transformers 
Sentence Transformers
Streamlit 




## summary : 

- chunking.py :- script handles the data ingestion step by loading 3–5 sample .txt files from the docs/ folder and splitting them into smaller, semantically meaningful chunks using RecursiveCharacterTextSplitter. These chunks are then prepared for vector embedding, ensuring better contextual retrieval during user queries.

- retriever.py :- module creates the vector search backbone using SentenceTransformers to embed the chunks and builds a FAISS vector index. It also defines a get_top_k_chunks(query) function to fetch the top 3 most relevant chunks for any given query, enabling the core RAG retrieval mecha

- rag_chain.py :- serves as the main CLI interface and implements an agentic workflow. Depending on the query, it routes to a calculator or dictionary tool if relevant keywords like "calculate" or "define" are detected. 

- app.py :- use for show streamlit (UI).