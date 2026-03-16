#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FRONTEND_DIR="${SCRIPT_DIR}/../frontend"

cd "${FRONTEND_DIR}"

if command -v npm >/dev/null 2>&1 && [ -s "package.json" ] && grep -q '"dev"' package.json; then
	exec npm run dev -- --host 0.0.0.0 "$@"
fi

echo "[run_frontend] npm is required to start the Vue dev server." >&2
exit 1
