#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}/../frontend"

cd "${FRONTEND_DIR}"

if command -v npm >/dev/null 2>&1 && [ -s "package.json" ] && grep -q '"dev"' package.json; then
	exec npm run dev -- --host 0.0.0.0 "$@"
fi

PORT="${PORT:-5173}"
echo "[run_frontend] npm dev script not ready, fallback to python static server on port ${PORT}" >&2
exec python3 -m http.server "${PORT}"
