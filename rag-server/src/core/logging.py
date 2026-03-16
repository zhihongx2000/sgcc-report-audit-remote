"""Structured JSON-lines logging setup for rag-server."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, TextIO

from core.constants import DEFAULT_LOG_LEVEL, DEFAULT_LOGGER_NAME, DEFAULT_SERVICE_NAME


_HANDLER_MARKER = "_a5_json_handler"


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


def setup_logging(
	*,
	logger_name: str = DEFAULT_LOGGER_NAME,
	level: str | int = DEFAULT_LOG_LEVEL,
	service_name: str = DEFAULT_SERVICE_NAME,
	stream: TextIO | None = None,
) -> logging.Logger:
	"""Create idempotent JSON-lines logger and return it."""
	logger = logging.getLogger(logger_name)
	logger.setLevel(_parse_level(level))
	logger.propagate = False

	for handler in logger.handlers:
		if getattr(handler, _HANDLER_MARKER, False):
			handler.setFormatter(JsonLinesFormatter(service_name=service_name))
			return logger

	handler = logging.StreamHandler(stream or sys.stdout)
	setattr(handler, _HANDLER_MARKER, True)
	handler.setFormatter(JsonLinesFormatter(service_name=service_name))
	logger.addHandler(handler)
	return logger
