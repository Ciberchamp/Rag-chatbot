from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from retriever import Retriever
from llm import LLMClient
from cache import Cache
import uvicorn

app = FastAPI(title="RAG HR Chatbot API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
retriever = Retriever()
llm_client = LLMClient()
cache = Cache()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: list

@app.post("/query", response_model=QueryResponse)
async def query_hr_bot(request: QueryRequest):
    try:
        # Check cache first
        cached_response = cache.get(request.question)
        if cached_response:
            return QueryResponse(**cached_response)
        
        # Retrieve relevant documents
        relevant_docs = retriever.search(request.question, top_k=3)
        
        # Generate answer using LLM
        answer = llm_client.generate_answer(request.question, relevant_docs)
        
        # Prepare sources
        sources = [doc['text'][:100] + "..." for doc in relevant_docs]
        
        response = QueryResponse(answer=answer, sources=sources)
        
        # Cache the response
        cache.set(request.question, response.dict())
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)