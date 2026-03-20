import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.cache = {}

    def load(self):
        if not self.model:
            self.model = SentenceTransformer(self.model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        to_encode = []
        for text in texts:
            if text not in self.cache:
                to_encode.append(text)
        
        if to_encode:
            embeddings = self.model.encode(to_encode)
            for text, emb in zip(to_encode, embeddings):
                self.cache[text] = emb
                
        # Return array mapping exact order
        return np.array([self.cache[t] for t in texts])

    def similarity_matrix(self, source: list[str], target: list[str]) -> np.ndarray:
        source_emb = self.encode(source)
        target_emb = self.encode(target)
        return cosine_similarity(source_emb, target_emb)

    def best_match(self, query: str, candidates: list[str]) -> tuple[str, float]:
        matrix = self.similarity_matrix([query], candidates)
        best_idx = np.argmax(matrix[0])
        return candidates[best_idx], float(matrix[0][best_idx])
