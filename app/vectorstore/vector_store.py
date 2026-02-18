import faiss
import numpy as np
import pickle
from typing import List


class FaissVectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []

    def add(self, vectors: List[List[float]], texts: List[str]):
        vecs = np.array(vectors, dtype="float32")
        faiss.normalize_L2(vecs)

        self.index.add(vecs)
        self.texts.extend(texts)

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

    def save(self, path: str):
        faiss.write_index(self.index, f"{path}.index")
        with open(f"{path}.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def load(self, path: str):
        self.index = faiss.read_index(f"{path}.index")
        with open(f"{path}.pkl", "rb") as f:
            self.texts = pickle.load(f)
