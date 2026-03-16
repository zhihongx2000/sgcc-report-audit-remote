from __future__ import annotations

import io
import json

import pytest

from sgcc_audit.core.logging import setup_logging


@pytest.mark.unit
def test_setup_logging_uses_yaml_defaults(tmp_path) -> None:
    stream = io.StringIO()
    config_path = tmp_path / "logging.yaml"
    config_path.write_text(
        "\n".join(
            [
                "service_name: sgcc-audit-backend",
                "logger_name: test.sgcc.audit",
                "level: INFO",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    logger = setup_logging(config_path=config_path, stream=stream)
    logger.info("request accepted", extra={"event": "request", "request_id": "req-42"})

    payload = json.loads(stream.getvalue().strip())
    assert payload["service"] == "sgcc-audit-backend"
    assert payload["logger"] == "test.sgcc.audit"
    assert payload["level"] == "INFO"
    assert payload["message"] == "request accepted"
    assert payload["event"] == "request"
    assert payload["request_id"] == "req-42"


@pytest.mark.unit
def test_setup_logging_is_idempotent_for_same_logger_name() -> None:
    logger_name = "test.sgcc.idempotent"
    logger = setup_logging(logger_name=logger_name)
    same_logger = setup_logging(logger_name=logger_name)

    assert same_logger is logger
    assert len(logger.handlers) == 1
