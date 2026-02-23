"""
Sports Analytics Assistant - FastAPI backend.
"""
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.scraper import scrape_player_game_logs
from app.metrics import fantasy_averages
from app.prompt_builder import build_prompt, build_comparison_prompt
from app.ollama_client import ask_ollama

app = FastAPI(
    title="Sports Analytics API",
    description="Backend for StatMuse scraping, fantasy metrics, prompt building, and Ollama.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://sports-analytics-assistant.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Body for POST /query."""

    player: str
    query: str


class CompareRequest(BaseModel):
    """Body for POST /compare."""

    player1: str
    player2: str
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


@app.post("/api/compare")
async def compare(request: CompareRequest):
    """
    Scrape both players' game logs in parallel, compute fantasy averages for each,
    build a comparison prompt, send to Ollama, and return the response.
    """
    games1, games2 = await asyncio.gather(
        scrape_player_game_logs(request.player1),
        scrape_player_game_logs(request.player2),
    )

    if not games1:
        raise HTTPException(
            status_code=404,
            detail=f"No game logs found for player: {request.player1}",
        )
    if not games2:
        raise HTTPException(
            status_code=404,
            detail=f"No game logs found for player: {request.player2}",
        )

    avgs1 = fantasy_averages(games1)
    avgs2 = fantasy_averages(games2)

    prompt = build_comparison_prompt(
        player1_name=request.player1,
        player2_name=request.player2,
        games1=games1,
        games2=games2,
        fantasy_avgs1=avgs1,
        fantasy_avgs2=avgs2,
        user_query=request.query,
    )

    try:
        response_text = await ask_ollama(prompt)
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Ollama request failed: {e!s}. Is Ollama running at localhost:11434?",
        ) from e

    return {"response": response_text}
