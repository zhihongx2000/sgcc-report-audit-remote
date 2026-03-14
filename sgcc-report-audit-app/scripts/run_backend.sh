#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="${SCRIPT_DIR}/../backend"

cd "${BACKEND_DIR}"
export PYTHONPATH="${BACKEND_DIR}/src:${PYTHONPATH:-}"

if command -v uv >/dev/null 2>&1; then
	if [ -f "pyproject.toml" ] && grep -q '^\[project\]' pyproject.toml; then
		exec uv run python -m sgcc_audit.main "$@"
	fi
	echo "[run_backend] uv project metadata not initialized yet, fallback to python3" >&2
	exec python3 -m sgcc_audit.main "$@"
fi

echo "[run_backend] uv command not found, fallback to python3" >&2
exec python3 -m sgcc_audit.main "$@"
