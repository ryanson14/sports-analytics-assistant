# Sports Analytics Assistant

AI-powered sports analytics with a Next.js frontend and FastAPI backend.

## Project structure

```
SportsAnalytics/
├── frontend/                 # Next.js 14 (App Router, TypeScript)
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── globals.css
│   ├── package.json
│   ├── next.config.js
│   └── tsconfig.json
├── backend/                  # FastAPI
│   ├── main.py               # API entrypoint
│   ├── requirements.txt
│   └── app/
│       ├── scrapers/
│       │   └── statmuse.py   # StatMuse scraper (placeholder)
│       └── services/
│           ├── fantasy_metrics.py  # Fantasy metrics calculator (placeholder)
│           ├── prompt_builder.py   # Prompt builder (placeholder)
│           └── ollama_client.py    # Ollama client (placeholder)
└── README.md
```

## Run locally

**Backend (FastAPI)**  
From `backend/`:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

**Frontend (Next.js)**  
From `frontend/`:

```bash
npm install
npm run dev
```

App: http://localhost:3000

## Modules (placeholders)

- **StatMuse scraper** (`app/scrapers/statmuse.py`) – Search and fetch stats from StatMuse.
- **Fantasy metrics** (`app/services/fantasy_metrics.py`) – Compute fantasy points and projections.
- **Prompt builder** (`app/services/prompt_builder.py`) – Build LLM prompts with StatMuse + fantasy context.
- **Ollama client** (`app/services/ollama_client.py`) – Call local Ollama for model responses.