# embeddings.py
from google import genai
from vectorstore.vector_store import FaissVectorStore
# Initialize client
client = genai.Client()

# Supported Gemini embedding model
EMBEDDING_MODEL = "gemini-embedding-001"


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings for a list of text chunks using official Google Gemini SDK.
    """
    batch_size = 10
    embeddings = []

    # Gemini allows batch embedding in one call, but we'll do chunk-by-chunk for clarity
    for i in range(0, len(chunks), batch_size):
        try:
            batch = chunks[i: i + batch_size]
            result = client.models.embed_content(
                model=EMBEDDING_MODEL,
                contents=batch # list of one string
            )

            for vec in result.embeddings:
                embeddings.append(vec.values)

            print(f"✅ Embedded batch {i // batch_size + 1}")
        except Exception as e:
            print(f"❌ Failed to embed chunk {i}: {e}")

    return embeddings
