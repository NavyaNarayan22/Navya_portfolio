import os
import sys
sys.path.append(os.path.dirname(__file__))

from fastapi import FastAPI
from pydantic import BaseModel
from pipeline import answer_question
from retriever import HybridRetriever

app = FastAPI(title="ArXiv RAG API")
retriever = HybridRetriever()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

@app.get("/")
def root():
    return {"status": "ok", "message": "ArXiv RAG API is running"}

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    result = answer_question(request.question, retriever)
    return QueryResponse(
        question=request.question,
        answer=result["answer"],
        sources=list(set(result["sources"])),
    )

@app.get("/health")
def health():
    return {"status": "healthy"}