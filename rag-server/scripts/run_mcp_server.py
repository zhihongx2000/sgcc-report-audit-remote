#!/usr/bin/env python3
"""Minimal MCP server launcher entry for A2.

This script intentionally keeps startup logic lightweight so the project can
provide a runnable entrypoint before full MCP wiring is implemented.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
	"""Build CLI parser for MCP server launcher."""
	parser = argparse.ArgumentParser(description="Run SGCC RAG MCP server entrypoint")
	parser.add_argument(
		"--config",
		default="config/settings.yaml",
		help="Path to MCP server settings file",
	)
	parser.add_argument(
		"--health",
		action="store_true",
		help="Print health payload and exit",
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Validate startup arguments without running server loop",
	)
	parser.add_argument(
		"--version",
		action="store_true",
		help="Print launcher version and exit",
	)
	return parser


def main(argv: list[str] | None = None) -> int:
	"""Script entrypoint for minimal MCP startup."""
	parser = build_parser()
	args = parser.parse_args(argv)

	if args.version:
		print("sgcc-rag-mcp-launcher 0.1.0")
		return 0

	if args.health:
		payload = {
			"status": "ok",
			"service": "rag-mcp-server",
			"transport": "stdio",
		}
		print(json.dumps(payload, ensure_ascii=True))
		return 0

	config_path = Path(args.config)
	if args.dry_run:
		state = "found" if config_path.exists() else "missing"
		print(f"[dry-run] config={config_path} ({state})", file=sys.stderr)
		return 0

	# Real MCP loop wiring will be introduced in later tasks.
	print(
		"MCP launcher entry is available. Use --health/--dry-run now; full server loop will be wired in later tasks.",
		file=sys.stderr,
	)
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
