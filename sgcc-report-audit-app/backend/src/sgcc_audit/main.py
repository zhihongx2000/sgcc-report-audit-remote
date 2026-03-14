"""Minimal backend entrypoint for A2.

Provides:
- create_app() for framework integration
- CLI startup path with --help support
- /health endpoint (FastAPI when available)
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any

try:
	from fastapi import FastAPI
except ImportError:  # pragma: no cover - dependency will be added in later task.
	FastAPI = None  # type: ignore[assignment]


class _FallbackAsgiApp:
	"""ASGI fallback app used before FastAPI dependency is installed."""

	async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
		if scope.get("type") != "http":
			return

		path = scope.get("path", "")
		if path == "/health":
			body = json.dumps({"status": "ok", "service": "sgcc-audit-backend"}).encode("utf-8")
			headers = [(b"content-type", b"application/json")]
			await send({"type": "http.response.start", "status": 200, "headers": headers})
			await send({"type": "http.response.body", "body": body})
			return

		await send({"type": "http.response.start", "status": 404, "headers": []})
		await send({"type": "http.response.body", "body": b"Not Found"})


def create_app() -> Any:
	"""Create backend app instance.

	Returns FastAPI app when dependency is available, otherwise returns a
	tiny fallback ASGI app so startup path is still executable.
	"""
	if FastAPI is None:
		return _FallbackAsgiApp()

	app = FastAPI(title="SGCC Report Audit Backend", version="0.1.0")

	@app.get("/health")
	async def health() -> dict[str, str]:
		return {"status": "ok", "service": "sgcc-audit-backend"}

	return app


def _build_parser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description="Run SGCC backend service")
	parser.add_argument("--host", default="0.0.0.0", help="Bind host")
	parser.add_argument("--port", type=int, default=8080, help="Bind port")
	parser.add_argument("--reload", action="store_true", help="Enable auto reload")
	parser.add_argument(
		"--print-health",
		action="store_true",
		help="Print health payload and exit",
	)
	return parser


def _run_with_uvicorn(app: Any, host: str, port: int, reload_enabled: bool) -> bool:
	try:
		import uvicorn
	except ImportError:
		return False

	uvicorn.run(app, host=host, port=port, reload=reload_enabled)
	return True


def main(argv: list[str] | None = None) -> int:
	parser = _build_parser()
	args = parser.parse_args(argv)

	if args.print_health:
		print(json.dumps({"status": "ok", "service": "sgcc-audit-backend"}, ensure_ascii=True))
		return 0

	app = create_app()
	started = _run_with_uvicorn(app=app, host=args.host, port=args.port, reload_enabled=args.reload)
	if not started:
		print(
			"uvicorn is not installed yet. Entry path is ready; install dependencies in A3/B1 then rerun.",
			file=sys.stderr,
		)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
