#rag pipeline made for seculding front end interaction
from prompts.search import semantic_search
from vectorstore.vector_store import FaissVectorStore
from prompts.rag import generate_rag_answer
import os

DIM = 3072

#absolute path needed for streamlit
# Get the directory where THIS file is located
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
STORE_PATH = os.path.join(THIS_DIR, "..", "data", "faiss_store")

#STORE_PATH = "../data/faiss_store" <--- relative path
def rag_answer(query: str, top_k: int = 3, temperature: float = 0.2):
    # 1. Load vector store
    store = FaissVectorStore(dim=DIM)
    store.load(STORE_PATH)

    # 2. Retrieve relevant chunks
    retrieved = semantic_search(store, query, top_k)

    # 3. Build sources (for UI)
    sources = []
    for r in retrieved:
        sources.append(
            f"{r['text'][:8]} | Rank {r['rank']} | Distance {r['distance']:.4f}"
        )

    # 4. Generate grounded answer
    answer = generate_rag_answer(
        query=query,
        retrieved_chunks=retrieved,
        temperature=temperature
    )

    return answer, sources