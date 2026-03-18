
import os
import chromadb
from sentence_transformers import SentenceTransformer
from typing import Optional
import logging

#  Ensure log folder
log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
os.makedirs(log_dir, exist_ok=True)  # Create logs folder if it doesn't exist

log_file = os.path.join(log_dir, "vector_db.log")

#  Configure logging with absolute path
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class VectorStore:
    def __init__(self):
        try:
            self.client = chromadb.PersistentClient(path="db/")
            self.collection = self.client.get_or_create_collection("automation_functions")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self._initialize_db()
            logging.info("VectorStore initialized successfully")
        except Exception as e:
            logging.error(f"VectorStore initialization failed: {e}")
            raise

    def _initialize_db(self):
        """Preload function metadata with enhanced descriptions."""
        functions = [
            {"name": "open_chrome", "description": "Open Google Chrome web browser"},
            {"name": "open_calculator", "description": "Launch system calculator application"},
            {"name": "get_cpu_usage", "description": "Check current CPU utilization percentage"},
            {"name": "run_shell_command", "description": "Execute terminal/shell commands"},
        ]
        try:
            self.collection.add(
                documents=[func["description"] for func in functions],
                metadatas=[{"name": func["name"]} for func in functions],
                ids=[func["name"] for func in functions]
            )
            logging.info("Loaded function metadata into ChromaDB")
        except Exception as e:
            logging.error(f"Failed to initialize DB: {e}")
            raise

    def retrieve_function(self, query: str) -> Optional[str]:
        """Enhanced retrieval with error handling."""
        try:
            query_embedding = self.embedding_model.encode(query).tolist()
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=1
            )
            if results["metadatas"]:
                return results["metadatas"][0][0]["name"]
            logging.warning(f"No function found for query: '{query}'")
            return None
        except Exception as e:
            logging.error(f"Retrieval error for query '{query}': {e}")
            return None
