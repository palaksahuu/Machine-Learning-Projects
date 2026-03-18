import os
import torch
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline

from langchain_community.vectorstores import FAISS
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

# load vectorstore from disk
def load_vectorstore(persist_path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(persist_path, embeddings, allow_dangerous_deserialization=True)
    return vectorstore

# external tool function
def call_external_tool(query):
    if "calculate" in query:
        expression = query.split("calculate")[-1].strip()
        return eval(expression) 
    elif "define" in query:
        return "This is a placeholder definition for the term."
    return "No tool matched for this query."

# RAG  LLM Pipeline with agentic 
def run_rag_llm_pipeline(query):
    use_tool = "calculate" in query or "define" in query
    print(f" Agent Decision: Routed to {'Tool' if use_tool else 'RAG Pipeline'} based on keyword match.")

    if use_tool:
        result = call_external_tool(query)
        print("\n Answer (from tool):", result)
    else:
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2}) 

        # load tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        model = AutoModelForCausalLM.from_pretrained("gpt2")

        # Updated pipeline with max_new_tokens 
        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if torch.cuda.is_available() else -1,
            max_new_tokens=500,
            truncation=True,
            return_full_text=True,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95
        )

        hf_llm = HuggingFacePipeline(pipeline=pipe)

        qa = RetrievalQA.from_chain_type(
            llm=hf_llm,
            retriever=retriever,
            return_source_documents=True
        )
        result = qa.invoke({"query": query})

        print("\n Answer:")
        print(result["result"])

        print("\n Source Documents:")
        for i, doc in enumerate(result["source_documents"]):
            print(f"\nSource #{i+1}:")
            print("File:", doc.metadata.get("source", "Unknown"))
            print("Content:", doc.page_content[:300], "...\n")

if __name__ == "__main__":
    user_query = input("Enter your query: ")
    run_rag_llm_pipeline(user_query)
