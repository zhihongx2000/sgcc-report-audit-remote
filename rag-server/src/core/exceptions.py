"""Application exceptions and normalized error payload helpers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from core.constants import ERROR_RESPONSE_KEY, ERROR_STATUS_BY_CODE, ErrorCode


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
