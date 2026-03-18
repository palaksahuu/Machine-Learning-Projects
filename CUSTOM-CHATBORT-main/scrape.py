import requests
from langchain_community.document_loaders import WebBaseLoader

def scrape_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}
    loader = WebBaseLoader(url, requests_per_second=1, requests_kwargs={"headers": headers})
    docs = loader.load()
    
    # Check if any content
    if not docs:
        raise ValueError("No data retrieved from the given URL.")
    
    return "\n".join([doc.page_content for doc in docs])

if __name__ == "__main__":
    url = "https://brainlox.com/courses/category/technical"
    try:
        scraped_data = scrape_data(url)
        with open("data.txt", "w", encoding="utf-8") as f:
            f.write(scraped_data)
        print(" Data Scraped Successfully!")
    except Exception as e:
        print(f" Error: {e}")
