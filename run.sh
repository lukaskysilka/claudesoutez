#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
#  Movit Energy — Market Size Estimator  |  One-click launcher
#  Usage: ./run.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# ── Colors ────────────────────────────────────────────────────────────────────
GRN="\033[0;32m"; YLW="\033[0;33m"; RED="\033[0;31m"; BLD="\033[1m"; RST="\033[0m"
ok()   { echo -e "${GRN}✓${RST} $*"; }
warn() { echo -e "${YLW}⚠${RST}  $*"; }
err()  { echo -e "${RED}✗${RST}  $*"; }

echo -e "\n${BLD}Movit Energy — Market Size Estimator${RST}"
echo "────────────────────────────────────────"

# ── Step 1: .env setup ────────────────────────────────────────────────────────
if [ ! -f "$ROOT/.env" ]; then
  cp "$ROOT/.env.example" "$ROOT/.env"
  warn ".env not found — created from template."
fi

# Check if placeholder key is still there
if grep -q "your_serper_api_key_here" "$ROOT/.env"; then
  echo ""
  warn "SERPER_API_KEY is not set yet."
  echo -e "  Get a free key at ${BLD}https://serper.dev${RST} (2 500 searches free)"
  echo ""
  printf "  Paste your Serper API key: "
  read -r SERPER_KEY
  if [ -z "$SERPER_KEY" ]; then
    err "No key entered. Edit .env manually and run ./run.sh again."
    exit 1
  fi
  # Replace placeholder in .env
  sed -i "s|your_serper_api_key_here|${SERPER_KEY}|" "$ROOT/.env"
  ok "API key saved to .env"
fi

# ── Step 2: Docker check ──────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
  err "Docker not found. Install Docker Desktop from https://docker.com and re-run."
  exit 1
fi
if ! docker info &>/dev/null; then
  err "Docker daemon is not running. Start Docker Desktop and re-run."
  exit 1
fi

# ── Step 3: Build & Start ─────────────────────────────────────────────────────
echo ""
echo -e "${BLD}Starting services…${RST} (first run builds images — takes ~1 min)"
echo ""

docker compose up --build -d

# ── Step 4: Wait for frontend to be ready ────────────────────────────────────
echo -ne "  Waiting for app to be ready"
for i in $(seq 1 30); do
  if curl -sf http://localhost:5173 &>/dev/null; then
    break
  fi
  echo -n "."
  sleep 2
done
echo ""

# ── Step 5: Open browser ─────────────────────────────────────────────────────
URL="http://localhost:5173"
ok "Backend  → http://localhost:8000"
ok "Frontend → ${URL}"
echo ""

# Try to open browser (Linux/macOS/WSL)
if command -v xdg-open &>/dev/null; then
  xdg-open "$URL" &>/dev/null &
elif command -v open &>/dev/null; then
  open "$URL"
elif command -v wslview &>/dev/null; then
  wslview "$URL"
fi

echo -e "${GRN}${BLD}App is running!${RST} Open ${BLD}${URL}${RST} in your browser."
echo ""
echo "  Useful commands:"
echo "    docker compose logs -f        # live logs"
echo "    docker compose down           # stop"
echo "    docker compose restart        # restart"
echo ""
