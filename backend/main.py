from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import GenerateRequest, GenerateResponse
from llm_service import generate_test_cases
from dotenv import load_dotenv

load_dotenv() # Load variables from .env if present

app = FastAPI(title="AI Test Case Generator MVP")

import os

# Configure CORS so the Next.js frontend can communicate
# We allow * to ensure no CORS issues during MVP deployment. 
# IN PRODUCTION: Replace "*" with your actual Vercel frontend URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for MVP simplicity
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_endpoint(request: GenerateRequest):
    """
    Synchronous endpoint that blocks to generate test cases 
    using the LangChain 5-Lens pipeline.
    """
    if not request.user_story or len(request.user_story.strip()) < 10:
        raise HTTPException(status_code=400, detail="User story is too short or empty.")
        
    result = await generate_test_cases(
        user_story=request.user_story,
        provider=request.provider
    )
    
    return result

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
