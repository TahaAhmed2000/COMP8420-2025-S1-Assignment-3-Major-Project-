# macquarie_rag_qa/app/routes/qa.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.rag_pipeline import answer_query

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):
    try:
        answer, sources = answer_query(request.question)
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))