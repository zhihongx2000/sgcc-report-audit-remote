from __future__ import annotations

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from sgcc_audit.core.constants import ErrorCode
from sgcc_audit.core.exceptions import AppError, register_exception_handlers


@pytest.mark.unit
@pytest.mark.asyncio
async def test_app_error_maps_to_expected_http_status() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/boom")
    async def boom() -> dict[str, str]:
        raise AppError(
            message="document missing",
            code=ErrorCode.NOT_FOUND,
            details={"document_id": "doc-404"},
        )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/boom", headers={"x-request-id": "req-7"})

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "NOT_FOUND",
            "message": "document missing",
            "details": {"document_id": "doc-404"},
            "request_id": "req-7",
        }
    }


@pytest.mark.unit
@pytest.mark.asyncio
async def test_unhandled_exception_is_normalized() -> None:
    app = FastAPI()
    register_exception_handlers(app)

    @app.get("/explode")
    async def explode() -> dict[str, str]:
        raise RuntimeError("unexpected")

    async with AsyncClient(transport=ASGITransport(app=app, raise_app_exceptions=False), base_url="http://test") as client:
        response = await client.get("/explode")

    assert response.status_code == 500
    assert response.json() == {
        "error": {
            "code": "INTERNAL_ERROR",
            "message": "internal server error",
            "details": {},
        }
    }
