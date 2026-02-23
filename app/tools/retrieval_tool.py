from prompts.search import semantic_search
from vectorstore.vector_store import FaissVectorStore
import os

DIM = 3072

#absolute path needed for streamlit
# Get the directory where THIS file is located
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(THIS_DIR, "..", "..", "data", "faiss_store")

#STORE_PATH = "../data/faiss_store" <--- relative path
def search_knowledge_base(query: str, top_k: int = 3):
    #Loads the vector store
    store = FaissVectorStore(dim=DIM)
    store.load(STORE_PATH)

    #retrieve relevant chunks by doing a semantic search in the store
    retrieved = semantic_search(store, query, top_k)

    return retrieved
