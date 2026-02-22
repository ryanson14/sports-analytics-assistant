"use client";

import { useState, FormEvent } from "react";

const API_QUERY = "https://sports-analytics-assistant-production.up.railway.app/api/query";
const API_COMPARE = "https://sports-analytics-assistant-production.up.railway.app/api/compare";

type Mode = "single" | "compare";

export default function Home() {
  const [mode, setMode] = useState<Mode>("single");
  const [player, setPlayer] = useState("");
  const [player1, setPlayer1] = useState("");
  const [player2, setPlayer2] = useState("");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setResponse(null);
    setLoading(true);

    const url = mode === "compare" ? API_COMPARE : API_QUERY;
    const body =
      mode === "compare"
        ? {
            player1: player1.trim(),
            player2: player2.trim(),
            query: query.trim(),
          }
        : { player: player.trim(), query: query.trim() };

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail ?? `Request failed (${res.status})`);
        return;
      }

      setResponse(data.response ?? "");
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to reach the backend. Is it running?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col items-center justify-center p-6 sm:p-8">
      {/* Subtle gradient and grid for depth */}
      <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(34,197,94,0.06)_0%,transparent_50%)] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(34,197,94,0.12),transparent)] pointer-events-none" />

      <div className="w-full max-w-lg relative">
        <header className="text-center mb-10">
          <h1 className="text-3xl sm:text-4xl font-bold tracking-tight text-white mb-2">
            Sports Analytics
          </h1>
          <p className="text-zinc-400 text-base sm:text-lg">
            AI-powered stats, fantasy value, and trends
          </p>
        </header>

        <form
          onSubmit={handleSubmit}
          className="bg-zinc-900/80 border border-zinc-800 rounded-2xl shadow-xl shadow-black/20 p-6 sm:p-8 space-y-6 backdrop-blur-sm"
        >
          <div className="flex rounded-xl bg-zinc-800/60 p-1">
            <button
              type="button"
              onClick={() => setMode("single")}
              className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                mode === "single"
                  ? "bg-zinc-700 text-white shadow"
                  : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              Single Player
            </button>
            <button
              type="button"
              onClick={() => setMode("compare")}
              className={`flex-1 py-2 px-3 rounded-lg text-sm font-medium transition-colors ${
                mode === "compare"
                  ? "bg-zinc-700 text-white shadow"
                  : "text-zinc-400 hover:text-zinc-200"
              }`}
            >
              Compare Players
            </button>
          </div>

          {mode === "single" ? (
            <div className="space-y-2">
              <label
                htmlFor="player"
                className="block text-sm font-medium text-zinc-300"
              >
                Player name
              </label>
              <input
                id="player"
                type="text"
                value={player}
                onChange={(e) => setPlayer(e.target.value)}
                placeholder="e.g. Tyrese Maxey, LeBron James"
                className="w-full px-4 py-3 bg-zinc-800/80 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500/50 transition-shadow"
                required
              />
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label
                  htmlFor="player1"
                  className="block text-sm font-medium text-zinc-300"
                >
                  Player 1
                </label>
                <input
                  id="player1"
                  type="text"
                  value={player1}
                  onChange={(e) => setPlayer1(e.target.value)}
                  placeholder="e.g. Tyrese Maxey"
                  className="w-full px-4 py-3 bg-zinc-800/80 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500/50 transition-shadow"
                  required={mode === "compare"}
                />
              </div>
              <div className="space-y-2">
                <label
                  htmlFor="player2"
                  className="block text-sm font-medium text-zinc-300"
                >
                  Player 2
                </label>
                <input
                  id="player2"
                  type="text"
                  value={player2}
                  onChange={(e) => setPlayer2(e.target.value)}
                  placeholder="e.g. LeBron James"
                  className="w-full px-4 py-3 bg-zinc-800/80 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500/50 transition-shadow"
                  required={mode === "compare"}
                />
              </div>
            </div>
          )}

          <div className="space-y-2">
            <label
              htmlFor="query"
              className="block text-sm font-medium text-zinc-300"
            >
              Question
            </label>
            <input
              id="query"
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask about stats, fantasy value, trends..."
              className="w-full px-4 py-3 bg-zinc-800/80 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/60 focus:border-emerald-500/50 transition-shadow"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 px-4 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-400 focus:ring-offset-2 focus:ring-offset-zinc-900 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:bg-emerald-600 transition-colors shadow-lg shadow-emerald-900/30"
          >
            {loading ? (mode === "compare" ? "Comparing…" : "Asking…") : mode === "compare" ? "Compare" : "Ask"}
          </button>
        </form>

        {(response !== null || error) && (
          <div
            className={`mt-8 rounded-2xl border p-5 sm:p-6 ${
              error
                ? "bg-red-950/40 border-red-800/60 text-red-200"
                : "bg-zinc-900/80 border-zinc-800 text-zinc-200"
            }`}
          >
            <h2 className="text-sm font-semibold uppercase tracking-wider mb-3 text-zinc-400">
              {error ? "Error" : "Response"}
            </h2>
            <div className="text-[15px] leading-relaxed whitespace-pre-wrap">
              {error ?? response}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
