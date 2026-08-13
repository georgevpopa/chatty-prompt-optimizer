from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from optimizer import optimize_prompt
from pathlib import Path
import os

app = FastAPI(title="Universal Prompt Optimizer")

class OptimizeRequest(BaseModel):
    raw_input: str
    target_model: str = "openai"

class OptimizeResponse(BaseModel):
    optimized_prompt: str

# --- NEW: Endpoint to serve the UI ---
@app.get("/", response_class=HTMLResponse)
async def get_ui():
    html_path = Path("index.html")
    if not html_path.exists():
        return HTMLResponse("<h1>Error: index.html not found</h1>", status_code=404)
    return HTMLResponse(content=html_path.read_text(), status_code=200)

# --- EXISTING: Endpoint for the backend logic ---
@app.post("/optimize", response_model=OptimizeResponse)
async def handle_optimize(request: OptimizeRequest):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY environment variable not set.")
    
    try:
        optimized = await optimize_prompt(
            raw_input=request.raw_input,
            target_model=request.target_model
        )
        return OptimizeResponse(optimized_prompt=optimized)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))