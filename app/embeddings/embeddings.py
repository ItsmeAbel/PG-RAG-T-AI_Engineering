# embeddings.py
from google import genai
import streamlit as st

api_key = st.secrets["GEMENI_API_KEY"]
# Initialize client
client = genai.Client(api_key=api_key)

#Gemini embedding model
EMBEDDING_MODEL = "gemini-embedding-001"


#function that can be called to do batch embeddings of chunks
def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks using official Google Gemini SDK.
    """
    batch_size = 10
    embeddings = []

   #uses gemeni model to do batch embedding. Embedds 10 chunks at a time
    for i in range(0, len(chunks), batch_size):
        try:
            batch = chunks[i: i + batch_size]
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch # list of one string
            )

            for vec in result.embeddings:
                embeddings.append(vec.values)

            print(f"Embedded batch {i // batch_size + 1}")
        except Exception as e:
            print(f"Failed to embed chunk {i}: {e}")

    return embeddings
