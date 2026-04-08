#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Movit Energy — Market Size Estimator  |  Quick Start
# Usage: ./start.sh
# ─────────────────────────────────────────────────────────────────────────────
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── Check .env ────────────────────────────────────────────────────────────────
if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  echo "⚠  Created .env from .env.example — add your SERPER_API_KEY before continuing."
  exit 1
fi

# ── Backend ───────────────────────────────────────────────────────────────────
echo "▶ Starting backend…"
cd "$ROOT/backend"
if [ ! -d ".venv" ]; then
  echo "  Creating Python virtualenv…"
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -q -r requirements.txt
cp "$ROOT/.env" .env 2>/dev/null || true
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "  Backend running (PID $BACKEND_PID) → http://localhost:8000"

# ── Frontend ──────────────────────────────────────────────────────────────────
echo "▶ Starting frontend…"
cd "$ROOT/frontend"
if [ ! -d "node_modules" ]; then
  echo "  Installing npm packages…"
  npm install
fi
npm run dev &
FRONTEND_PID=$!
echo "  Frontend running (PID $FRONTEND_PID) → http://localhost:5173"

echo ""
echo "✓ Both services started. Open http://localhost:5173 in your browser."
echo "  Press Ctrl+C to stop."

# ── Cleanup on exit ───────────────────────────────────────────────────────────
trap "echo ''; echo 'Stopping…'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0" INT TERM
wait
