# main.py
from ingestion.load_json import load_json
from ingestion.chunking import chunk_json_record
from embeddings.embeddings import embed_chunks
from vectorstore.vector_store import FaissVectorStore
from prompts.search import semantic_search
from prompts.rag import generate_rag_answer

data = load_json("../data/incidents.json")

all_chunks = []
embeddings = []

#main function used during the first steps of building the app.
#Not used for the actuall app in the final stages
#can however be used to update the vector store if the input content changes
# ----------------chunking----------------
# each record in the json becomes a chunk
def main_chunk():
    for record in data:
        chunks = chunk_json_record(record)
        all_chunks.extend(chunks)

    print(f"Generated {len(all_chunks)} chunks")
    print(all_chunks[:2])


# ----------Embeddings----------------------
def main_embed():
    embeddings = embed_chunks(all_chunks)

    print("\nSample embedding vector (first 5 values):")
    print(embeddings[:5])


# ----------Vectore Storing-------------

DIM = 3072
STORE_PATH = "../data/faiss_store"


#build the vector store, either upon first time running the program or changing the json file
def build_and_save_store():

    store = FaissVectorStore(dim=DIM)
    store.add(embeddings, all_chunks)
    store.save(STORE_PATH)

    print("✅ Vector store built and saved")


# ------search-----
# used for testing and verifies vector store query searching functionalities. 
# Add 'load_and_query_store()' in the main runner below to test and verify
def load_and_query_store():

    store = FaissVectorStore(dim=DIM)
    store.load(STORE_PATH)

    print("FAISS vectors:", store.index.ntotal)
    print("Texts stored:", len(store.texts))

    queries = [
        "ssl certificate expired",
        "database connection pool exhaustion",
        "high severity incident caused by permissions",
    ]

    for q in queries:
        results = semantic_search(store, q)

        print(f"\nQUERY: {q}")
        for r in results:
            print(f"\nRank {r['rank']} | Distance: {r['distance']:.4f}")
            print(r["text"][:400])


# -------------RAG Pipeline------------
def rag_query(query: str, k: int = 5):
    store = FaissVectorStore(dim=DIM)
    store.load(STORE_PATH)

    retrieved = semantic_search(store, query, k)

    print("\n🔍 Retrieved Chunks:")
    for r in retrieved:
        print(f"\nRank {r['rank']} | Distance {r['distance']:.4f}")
        print(r["text"][:300])

    answer = generate_rag_answer(query, retrieved)

    print("\n🤖 RAG Answer:")
    print(answer)
    return answer


# -------------Overlapp check--------------------------------------
# used for inspecing overlap behavior. if last 10 words of a chunk(i) are the same as first 10 words of chunk(i+1) then overlap works
def main_overlap_check():
    for i, chunk in enumerate(all_chunks):
        words = chunk.split()

        print(f"\n=== CHUNK {i + 1} ===")
        print("First 10 words:", " ".join(words[:10]))
        print("Last 10 words: ", " ".join(words[-10:]))


# -------------chunking sanity check-------------------------
def main_sanity_check():

    # inspects chunk length distribution
    lengths = [len(chunk.split()) for chunk in all_chunks]

    print("Min words:", min(lengths))
    print("Max words:", max(lengths))
    print("Avg words:", sum(lengths) / len(lengths))


# Example Query: "Have we ever had a DDOS attack and how was it resolved and what was the outcome?"
if __name__ == "__main__":
    qry = input()
    rag_query(qry)
