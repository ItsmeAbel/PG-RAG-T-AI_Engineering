import faiss
import numpy as np
import pickle
from typing import List


class FaissVectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []
#used to add new vectors in the store
    def add(self, vectors: List[List[float]], texts: List[str]):
        vecs = np.array(vectors, dtype="float32")
        faiss.normalize_L2(vecs)

        self.index.add(vecs)
        self.texts.extend(texts)

#used for searching vecotrs in the store. Uses semantic search and ANN to identify the closes neigbours
    def search(self, query_vector: List[float], k: int = 3):
        q = np.array(query_vector, dtype="float32").reshape(1, -1)
        faiss.normalize_L2(q)

        distances, indices = self.index.search(q, k)

        results = []
        for i, idx in enumerate(indices[0]):
            results.append(
                {
                    "rank": i + 1,
                    "distance": float(distances[0][i]),
                    "text": self.texts[idx],
                }
            )
        return results

#saves the store into a pickle file
    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.pkl", "wb") as f:
            pickle.dump(self.texts, f)
#loads the store from a saved pickle file
    def load(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.pkl", "rb") as f:
            self.texts = pickle.load(f)
