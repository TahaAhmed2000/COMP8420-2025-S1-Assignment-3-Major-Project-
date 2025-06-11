# macquarie_rag_qa/app/utils/loader.py
import pandas as pd

def load_dataset(csv_paths):
    dfs = []
    for path in csv_paths:
        df = pd.read_csv(path)
        # Ensure required columns exist
        for col in ["category", "title", "answer", "url"]:
            if col not in df.columns:
                raise ValueError(f"Missing column '{col}' in {path}")
        df["text"] = df["title"].fillna("") + ". " + df["answer"].fillna("")
        dfs.append(df)
    
    return pd.concat(dfs, ignore_index=True)