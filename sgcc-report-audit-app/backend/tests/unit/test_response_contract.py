from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from sgcc_audit.schemas.response_models import build_backend_contract_snapshot


def _read_docs_snapshot() -> dict[str, list[str]]:
    repo_root = Path(__file__).resolve().parents[4]
    doc_path = repo_root / "docs" / "api" / "sgcc-backend-openapi.md"
    markdown = doc_path.read_text(encoding="utf-8")

    match = re.search(
        r"<!-- CONTRACT_FIELD_SNAPSHOT_BEGIN -->[\s\S]*?```json\s*([\s\S]*?)\s*```[\s\S]*?<!-- CONTRACT_FIELD_SNAPSHOT_END -->",
        markdown,
    )
    if not match:
        raise AssertionError("contract snapshot block not found in sgcc-backend-openapi.md")

    return json.loads(match.group(1))


@pytest.mark.unit
def test_contract_snapshot_is_valid_json() -> None:
    snapshot = _read_docs_snapshot()

    assert "ApiEnvelope" in snapshot
    assert "TraceRecord" in snapshot
    assert "EvaluationRunRecord" in snapshot


@pytest.mark.unit
def test_backend_response_models_match_docs_snapshot() -> None:
    docs_snapshot = _read_docs_snapshot()
    backend_snapshot = build_backend_contract_snapshot()

    assert backend_snapshot == docs_snapshot
