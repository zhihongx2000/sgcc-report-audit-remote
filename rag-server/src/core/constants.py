"""Shared constants for error handling and structured logging."""

from __future__ import annotations

from enum import StrEnum


DEFAULT_SERVICE_NAME = "rag-mcp-server"
DEFAULT_LOGGER_NAME = "rag_server"
DEFAULT_LOG_LEVEL = "INFO"


class ErrorCode(StrEnum):
	"""Canonical application error codes."""

	INVALID_ARGUMENT = "INVALID_ARGUMENT"
	UNAUTHORIZED = "UNAUTHORIZED"
	FORBIDDEN = "FORBIDDEN"
	NOT_FOUND = "NOT_FOUND"
	CONFLICT = "CONFLICT"
	TIMEOUT = "TIMEOUT"
	INTERNAL_ERROR = "INTERNAL_ERROR"


ERROR_STATUS_BY_CODE: dict[ErrorCode, int] = {
	ErrorCode.INVALID_ARGUMENT: 400,
	ErrorCode.UNAUTHORIZED: 401,
	ErrorCode.FORBIDDEN: 403,
	ErrorCode.NOT_FOUND: 404,
	ErrorCode.CONFLICT: 409,
	ErrorCode.TIMEOUT: 504,
	ErrorCode.INTERNAL_ERROR: 500,
}

ERROR_RESPONSE_KEY = "error"
