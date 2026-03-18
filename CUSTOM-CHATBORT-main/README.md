
 CUSTOM CHATBOT 
 
1. Better Data Extraction 
   - The current method using `WebBaseLoader` may not extract structured content effectively.  
   - If the website has dynamic content, consider using **Selenium or BeautifulSoup**.  

2. Improved Embedding Storage 
   - Storing the entire scraped text as a single chunk reduces retrieval accuracy.  
   - Solution: **Break text into smaller chunks** using Langchain’s `RecursiveCharacterTextSplitter` for better search results.  

3. Security Enhancement
   - The `allow_dangerous_deserialization=True` setting in FAISS can pose security risks.  
   - Ensure the stored FAISS index remains unmodified to avoid potential vulnerabilities.  
Key Fixes Implemented**  
Updated `scrape.py` → Improved data extraction with error handling.  
Updated `create_embedding.py` → Splits text into meaningful chunks before storing embeddings.  
Updated `app.py` → Handles query errors properly and improves the chatbot's response accuracy.  

Next Steps
1. Run `scrape.py` to fetch and clean data.  
2. Run `create_embedding.py` to generate vector embeddings.  
3. Start the chatbot by running `app.py`.  

