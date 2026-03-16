from __future__ import annotations

import pytest

from core.constants import ErrorCode
from core.exceptions import AppError, normalize_exception, status_code_from_error


@pytest.mark.unit
def test_status_code_from_error_maps_expected_values() -> None:
    assert status_code_from_error(ErrorCode.INVALID_ARGUMENT) == 400
    assert status_code_from_error(ErrorCode.NOT_FOUND) == 404
    assert status_code_from_error(ErrorCode.INTERNAL_ERROR) == 500


@pytest.mark.unit
def test_app_error_to_payload_has_stable_shape() -> None:
    exc = AppError(
        message="document not found",
        code=ErrorCode.NOT_FOUND,
        details={"document_id": "doc-1"},
    )

    payload = exc.to_payload(request_id="req-123")

    assert exc.resolved_status_code == 404
    assert payload == {
        "error": {
            "code": "NOT_FOUND",
            "message": "document not found",
            "details": {"document_id": "doc-1"},
            "request_id": "req-123",
        }
    }


@pytest.mark.unit
def test_normalize_exception_wraps_unknown_errors() -> None:
    exc = normalize_exception(RuntimeError("boom"))

    assert isinstance(exc, AppError)
    assert exc.code is ErrorCode.INTERNAL_ERROR
    assert exc.message == "internal server error"
