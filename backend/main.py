"""
Sports Analytics Assistant - FastAPI backend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sports Analytics API",
    description="Backend for StatMuse scraping, fantasy metrics, prompt building, and Ollama.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Sports Analytics API", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


# Optional: mount routers or import placeholders so structure is discoverable
# from app.scrapers.statmuse import StatMuseScraper
# from app.services.fantasy_metrics import FantasyMetricsCalculator
# from app.services.prompt_builder import PromptBuilder
# from app.services.ollama_client import OllamaClient
