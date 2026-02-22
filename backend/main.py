"""
Sports Analytics Assistant - FastAPI backend.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.scraper import scrape_player_game_logs
from app.metrics import fantasy_averages
from app.prompt_builder import build_prompt
from app.ollama_client import ask_ollama

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


class QueryRequest(BaseModel):
    """Body for POST /query."""

    player: str
    query: str


@app.get("/")
def root():
    return {"message": "Sports Analytics API", "docs": "/docs"}


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/query")
async def query(request: QueryRequest):
    """
    Scrape player game logs from StatMuse, compute fantasy averages,
    build a prompt with the stats, send to Ollama, and return the response.
    """
    games = await scrape_player_game_logs(request.player)
    if not games:
        raise HTTPException(
            status_code=404,
            detail=f"No game logs found for player: {request.player}",
        )

    avgs = fantasy_averages(games)
    prompt = build_prompt(
        player_name=request.player,
        user_query=request.query,
        games=games,
        fantasy_avgs=avgs,
    )

    try:
        response_text = await ask_ollama(prompt)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama request failed: {e!s}. Is Ollama running at localhost:11434?",
        ) from e

    return {"response": response_text}
