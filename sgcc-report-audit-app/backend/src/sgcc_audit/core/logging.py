"""Structured JSON-lines logging setup for backend service."""

from __future__ import annotations

import json
import logging
from pathlib import Path
import sys
from datetime import datetime, timezone
from typing import Any, TextIO

import yaml

from sgcc_audit.core.constants import DEFAULT_LOG_LEVEL, DEFAULT_LOGGER_NAME, DEFAULT_SERVICE_NAME


_HANDLER_MARKER = "_a5_json_handler"
_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[4] / "config" / "logging.yaml"


class JsonLinesFormatter(logging.Formatter):
	"""Formatter that emits one JSON object per log line."""

	def __init__(self, *, service_name: str) -> None:
		super().__init__()
		self._service_name = service_name

	def format(self, record: logging.LogRecord) -> str:
		payload: dict[str, Any] = {
			"timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
			"level": record.levelname,
			"logger": record.name,
			"service": self._service_name,
			"message": record.getMessage(),
		}

		for key in ("event", "request_id", "trace_id", "error_code"):
			value = getattr(record, key, None)
			if value is not None:
				payload[key] = value

		if record.exc_info:
			payload["exception"] = self.formatException(record.exc_info)

		return json.dumps(payload, ensure_ascii=True)


def _parse_level(level: str | int) -> int:
	if isinstance(level, int):
		return level
	resolved = logging.getLevelName(level.upper())
	if isinstance(resolved, int):
		return resolved
	return logging.INFO


def _load_logging_config(config_path: str | Path | None) -> dict[str, Any]:
	path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
	if not path.exists():
		return {}

	with path.open("r", encoding="utf-8") as f:
		loaded = yaml.safe_load(f)

	if loaded is None:
		return {}
	if not isinstance(loaded, dict):
		raise ValueError(f"Logging config must contain a YAML mapping: {path}")
	return dict(loaded)


def setup_logging(
	*,
	config_path: str | Path | None = None,
	logger_name: str | None = None,
	service_name: str | None = None,
	level: str | int | None = None,
	stream: TextIO | None = None,
) -> logging.Logger:
	"""Create idempotent JSON-lines logger and return it."""
	config = _load_logging_config(config_path)
	resolved_logger_name = logger_name or str(config.get("logger_name", DEFAULT_LOGGER_NAME))
	resolved_service_name = service_name or str(config.get("service_name", DEFAULT_SERVICE_NAME))
	resolved_level = level if level is not None else str(config.get("level", DEFAULT_LOG_LEVEL))

	logger = logging.getLogger(resolved_logger_name)
	logger.setLevel(_parse_level(resolved_level))
	logger.propagate = False

	for handler in logger.handlers:
		if getattr(handler, _HANDLER_MARKER, False):
			handler.setFormatter(JsonLinesFormatter(service_name=resolved_service_name))
			return logger

	handler = logging.StreamHandler(stream or sys.stdout)
	setattr(handler, _HANDLER_MARKER, True)
	handler.setFormatter(JsonLinesFormatter(service_name=resolved_service_name))
	logger.addHandler(handler)
	return logger
