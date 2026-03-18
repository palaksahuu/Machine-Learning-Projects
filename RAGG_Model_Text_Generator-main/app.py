import streamlit as st
from rag_chain import run_rag_llm_pipeline, call_external_tool, load_vectorstore
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

# Set page config
st.set_page_config(page_title="RAG Q&A Assistant", layout="wide")

# Header
st.title("RAG-Powered Multi-Agent Q&A Assistant")

st.markdown("""
            
Welcome! Ask a question below, and the assistant will:
            
- Route to an external **Tool** (e.g., Calculator or Definition) if needed.
            
- Otherwise, use **RAG + LLM** to answer from internal knowledge base.
            
""")

# User input
query = st.text_input("Enter your question here:")

# Submit
if st.button("Submit Query") and query:
    with st.spinner("Thinking..."):

        use_tool = "calculate" in query or "define" in query

        # Agent Decision Display
        st.markdown(f"### Agent Decision: {'Tool' if use_tool else 'RAG Pipeline'}")

        if use_tool:
            # Tool Route
            tool_answer = call_external_tool(query)
            st.success("Answer from Tool:")
            st.markdown(f"**{tool_answer}**")

        else:
            # RAG Route
            vectorstore = load_vectorstore()
            retriever = vectorstore.as_retriever()

            # Load HF LLM
            hf_pipeline = pipeline("text-generation", model="gpt2", max_new_tokens=100)
            hf_llm = HuggingFacePipeline(pipeline=hf_pipeline)

            # Build RAG Chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=hf_llm,
                retriever=retriever,
                return_source_documents=True
            )

            # result = qa_chain(query)
            result = qa_chain.invoke(query)

            # Display Answer
            st.success("Answer from RAG + LLM:")
            st.markdown(f"**{result['result']}**")

            # Display Retrieved Chunks
            st.markdown("---")
            st.markdown("### 📚 Retrieved Source Chunks")
            for i, doc in enumerate(result['source_documents']):
                st.markdown(f"**Chunk #{i + 1}** — *{doc.metadata.get('source', 'Unknown')}*")
                st.code(doc.page_content[:500], language="markdown")

# # Footer
st.markdown("---")
st.caption("Built with LangChain, HuggingFace, and FAISS ")
