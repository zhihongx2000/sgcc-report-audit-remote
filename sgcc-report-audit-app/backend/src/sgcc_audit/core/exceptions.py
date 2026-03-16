"""Application exceptions and FastAPI response mapping."""

from __future__ import annotations

from dataclasses import dataclass, field
import logging
from typing import Any, Mapping

from sgcc_audit.core.constants import ERROR_RESPONSE_KEY, ERROR_STATUS_BY_CODE, ErrorCode

try:
	from fastapi import FastAPI, Request
	from fastapi.responses import JSONResponse
except ImportError:  # pragma: no cover - handled by A2 fallback runtime.
	FastAPI = None  # type: ignore[assignment]
	Request = None  # type: ignore[assignment]
	JSONResponse = None  # type: ignore[assignment]


def status_code_from_error(code: ErrorCode) -> int:
	"""Map canonical error code to HTTP status code."""
	return ERROR_STATUS_BY_CODE.get(code, 500)


@dataclass(slots=True)
class AppError(Exception):
	"""Base domain error carrying stable code and HTTP status mapping."""

	message: str
	code: ErrorCode = ErrorCode.INTERNAL_ERROR
	status_code: int | None = None
	details: Mapping[str, Any] = field(default_factory=dict)

	def __post_init__(self) -> None:
		Exception.__init__(self, self.message)

	@property
	def resolved_status_code(self) -> int:
		if self.status_code is not None:
			return self.status_code
		return status_code_from_error(self.code)

	def to_payload(self, *, request_id: str | None = None) -> dict[str, Any]:
		error = {
			"code": self.code.value,
			"message": self.message,
			"details": dict(self.details),
		}
		if request_id:
			error["request_id"] = request_id
		return {ERROR_RESPONSE_KEY: error}


def normalize_exception(exc: Exception) -> AppError:
	"""Convert unknown exceptions to a safe internal error object."""
	if isinstance(exc, AppError):
		return exc
	return AppError(message="internal server error", code=ErrorCode.INTERNAL_ERROR)


def register_exception_handlers(app: FastAPI, *, logger_name: str = "sgcc_audit") -> None:
	"""Register consistent JSON error mapping for backend APIs."""
	if JSONResponse is None:
		return

	logger = logging.getLogger(logger_name)

	@app.exception_handler(AppError)
	async def _handle_app_error(request: Request, exc: AppError) -> JSONResponse:
		request_id = request.headers.get("x-request-id")
		logger.warning(
			"application error",
			extra={
				"event": "app_error",
				"error_code": exc.code.value,
				"request_id": request_id,
			},
		)
		return JSONResponse(
			status_code=exc.resolved_status_code,
			content=exc.to_payload(request_id=request_id),
		)

	@app.exception_handler(Exception)
	async def _handle_unknown_error(request: Request, exc: Exception) -> JSONResponse:
		request_id = request.headers.get("x-request-id")
		normalized = normalize_exception(exc)
		logger.exception(
			"unhandled exception",
			extra={
				"event": "unhandled_exception",
				"error_code": normalized.code.value,
				"request_id": request_id,
			},
		)
		return JSONResponse(
			status_code=normalized.resolved_status_code,
			content=normalized.to_payload(request_id=request_id),
		)
