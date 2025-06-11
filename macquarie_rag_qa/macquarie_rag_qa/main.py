# macquarie_rag_qa/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai

from app.utils.embedder import EmbeddingIndexer
from app.utils.prompter import create_prompt

# === FastAPI App ===
app = FastAPI()

# === CORS Settings (allow frontend access) ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Consider tightening for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Gemini LLM Setup ===
genai.configure(api_key="AIzaSyAosBAdQBDeExWO6_0icpobNHrP9fWkTtE")
llm = genai.GenerativeModel("gemini-2.0-flash")

# === Initialize Index ===
embedding_indexer = EmbeddingIndexer()
embedding_indexer.load_index("data/index")  # Load FAISS + metadata

# === Request Schema ===
class AskRequest(BaseModel):
    question: str

# === POST /ask Endpoint ===
@app.post("/ask")
async def ask(request: AskRequest):
    question = request.question
    try:
        results = embedding_indexer.search(question, top_k=5)
        prompt = create_prompt(question, results)

        response = llm.generate_content(prompt)
        answer = response.text
        sources = [meta if isinstance(meta, str) else meta.get("url") for _, meta in results]

        return {
            "answer": answer,
            "sources": sources
        }
    except Exception as e:
        return {
            "answer": "❌ Internal Server Error",
            "error": str(e)
        }

# === GET / Health Check ===
@app.get("/")
def root():
    return {"message": "Macquarie QA System is live ✅"}