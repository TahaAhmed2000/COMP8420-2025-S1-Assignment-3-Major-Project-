# macquarie_rag_qa/app/utils/embedder.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class EmbeddingIndexer:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.texts = []
        self.metadata = []

    def create_index(self, texts, metadata, save_path="index"):
        self.texts = texts
        self.metadata = metadata

        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        # Save index and metadata
        os.makedirs(save_path, exist_ok=True)
        faiss.write_index(self.index, f"{save_path}/faiss.index")
        np.save(f"{save_path}/metadata.npy", metadata, allow_pickle=True)
        np.save(f"{save_path}/texts.npy", texts, allow_pickle=True)

    def load_index(self, path="index"):
        self.index = faiss.read_index(f"{path}/faiss.index")
        self.metadata = np.load(f"{path}/metadata.npy", allow_pickle=True).tolist()
        self.texts = np.load(f"{path}/texts.npy", allow_pickle=True).tolist()

    def search(self, query, top_k=3):
        embedding = self.model.encode([query])
        D, I = self.index.search(embedding, top_k)
        results = [(self.texts[i], self.metadata[i]) for i in I[0]]
        return results