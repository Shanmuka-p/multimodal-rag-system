from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

# Import our custom modules
from src.retrieval.retriever import Retriever
from src.generation.generator import VLMGenerator

# Initialize the API
app = FastAPI(title="Multimodal RAG API", version="1.0")

# Initialize our core components once (so we don't reload models on every request)
print("Initializing System Components...")
retriever = Retriever()
generator = VLMGenerator()
print("System Ready.")

# Define the data format for the user's request
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

# Define the data format for the API's response
class SourceItem(BaseModel):
    document_id: str
    page_number: int
    content_type: str
    snippet: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceItem]

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    End-to-end endpoint:
    1. Receives a user query.
    2. Retrieves relevant text and images.
    3. Generates an answer using Gemini.
    4. Returns the answer and sources.
    """
    try:
        # Step 1: Retrieve context
        retrieved_items = retriever.query(request.query, top_k=request.top_k)
        
        # Step 2: Generate Answer
        # We pass the raw context items to the generator
        answer = generator.generate_answer(request.query, retrieved_items)
        
        # Step 3: Format the sources for the response
        sources = []
        for item in retrieved_items:
            sources.append(SourceItem(
                document_id=item["source"],
                page_number=item["page"],
                content_type=item["type"],
                snippet=str(item["content"])[:200] + "..." # Truncate long content for cleaner logs
            ))
            
        return QueryResponse(answer=answer, sources=sources)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Simple endpoint to check if the server is running."""
    return {"status": "healthy"}

if __name__ == "__main__":
    # Run the server on localhost port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)