# main.py
from ingestion.load_json import load_json
from ingestion.chunking import chunk_json_record
from embeddings.embeddings import embed_chunks

data = load_json("../data/incidents.json")

all_chunks = []

#each record in the json becomes a chunk
for record in data:
    chunks = chunk_json_record(record)
    all_chunks.extend(chunks)


print(f"Generated {len(all_chunks)} chunks")
print(all_chunks[:2])

embeddings = embed_chunks(all_chunks)

print("\nSample embedding vector (first 5 values):")
print(embeddings[:5])


#used of inspecing overlap behavior. if last 10 words of a chunk(i) are the same as first 10 words of chunk(i+1) then overlap works
for i, chunk in enumerate(all_chunks):
    words = chunk.split()

    print(f"\n=== CHUNK {i + 1} ===")
    print("First 10 words:", " ".join(words[:10]))
    print("Last 10 words: ", " ".join(words[-10:]))

#inspects chunk length distribution
lengths = [len(chunk.split()) for chunk in all_chunks]

print("Min words:", min(lengths))
print("Max words:", max(lengths))
print("Avg words:", sum(lengths) / len(lengths))

