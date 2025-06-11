# macquarie_rag_qa/scripts/setup_index.py

from app.utils.loader import load_dataset
from app.utils.embedder import EmbeddingIndexer

# 👇 Just replace this with your final combined CSV path
csv_path = "data/all_macquarie_articles.csv"

# Load the single dataset
df = load_dataset([csv_path])  # It still expects a list

# Initialize the indexer
indexer = EmbeddingIndexer()

# Create and save the FAISS index
indexer.create_index(
    texts=df["text"].tolist(),      # Full content for embedding
    metadata=df["url"].tolist(),    # We'll use URL as reference
    save_path="index"               # Folder where index & metadata is saved
)