from __future__ import annotations

import io
import json

import pytest

from core.logging import setup_logging


@pytest.mark.unit
def test_setup_logging_emits_json_lines_payload() -> None:
    stream = io.StringIO()
    logger = setup_logging(
        logger_name="test.rag.json",
        service_name="rag-mcp-server",
        level="INFO",
        stream=stream,
    )

    logger.info(
        "pipeline started",
        extra={"event": "pipeline_start", "request_id": "req-001"},
    )

    payload = json.loads(stream.getvalue().strip())
    assert payload["service"] == "rag-mcp-server"
    assert payload["level"] == "INFO"
    assert payload["message"] == "pipeline started"
    assert payload["event"] == "pipeline_start"
    assert payload["request_id"] == "req-001"


@pytest.mark.unit
def test_setup_logging_is_idempotent_for_same_logger() -> None:
    logger_name = "test.rag.idempotent"
    logger = setup_logging(logger_name=logger_name)
    same_logger = setup_logging(logger_name=logger_name)

    assert same_logger is logger
    assert len(logger.handlers) == 1
