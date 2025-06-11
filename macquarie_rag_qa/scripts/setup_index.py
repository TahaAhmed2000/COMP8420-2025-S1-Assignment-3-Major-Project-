# macquarie_rag_qa/scrripts/setup_index.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pandas as pd
from app.utils.embedder import EmbeddingIndexer

# === Config ===
CSV_PATH = "data/all_macquarie_articles.csv"  # Update this if your file is named differently
INDEX_DIR = "data/index"

# === Step 1: Load CSV ===
def load_dataset(path):
    df = pd.read_csv(path)
    df.dropna(subset=["answer"], inplace=True)  # Ensure no missing text
    return df

# === Step 2: Build index ===
def main():
    print("📦 Loading dataset...")
    df = load_dataset(CSV_PATH)

    texts = df["answer"].astype(str).tolist()

    # Store source URL and title as metadata for traceability
    metadata = df[["title", "url"]].to_dict(orient="records")

    print("🧠 Generating embeddings and indexing...")
    indexer = EmbeddingIndexer()
    indexer.create_index(texts, metadata, save_path=INDEX_DIR)

    print(f"✅ Index built and saved to '{INDEX_DIR}'")

if __name__ == "__main__":
    main()