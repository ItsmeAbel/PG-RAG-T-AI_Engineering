import numpy as np
from google import genai
from vectorstore.vector_store import FaissVectorStore
import streamlit as st

api_key = st.secrets["GEMENI_API_KEY"]
EMBEDDING_MODEL = "gemini-embedding-001"
client = genai.Client(api_key=api_key)


# uses the a gemini model to transform user query into embeddings
def embed_query(query: str) -> list[float]:
    result = client.models.embed_content(model=EMBEDDING_MODEL, contents=[query])
    return result.embeddings[0].values

# uses these new embeddings to perform a semantic search in the vector store
def semantic_search(store: FaissVectorStore, query: str, k):
    q_vec = embed_query(query)
    return store.search(q_vec, k)
