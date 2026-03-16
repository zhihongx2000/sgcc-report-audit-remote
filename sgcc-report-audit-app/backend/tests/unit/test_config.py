from __future__ import annotations

import textwrap

import pytest
from pydantic import ValidationError

from sgcc_audit.core.config import Settings, get_config, load_settings


def _write_settings_file(tmp_path, content: str):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return config_path


@pytest.mark.unit
def test_get_config_loads_default_file() -> None:
    settings = get_config(force_reload=True)

    assert isinstance(settings, Settings)
    assert settings.service_name == "sgcc-audit-backend"
    assert settings.llm.provider == "qwen"


@pytest.mark.unit
def test_load_settings_env_overrides_key_fields(monkeypatch, tmp_path) -> None:
    config_path = _write_settings_file(
        tmp_path,
        """
        service_name: sgcc-audit-backend
        environment: development
        mcp_client:
          command: uv run python rag-server/scripts/run_mcp_server.py
          timeout_seconds: 30
        llm:
          provider: local
          model: local-model
          api_key: local-key
          timeout_seconds: 10
        """,
    )

    monkeypatch.setenv("SGCC_BACKEND_LLM_PROVIDER", "azure_openai")
    monkeypatch.setenv("SGCC_BACKEND_LLM_TIMEOUT_SECONDS", "60")

    settings = load_settings(config_path)

    assert settings.llm.provider == "azure_openai"
    assert settings.llm.timeout_seconds == 60
    assert settings.llm.model == "local-model"


@pytest.mark.unit
def test_load_settings_missing_required_field_raises(tmp_path) -> None:
    config_path = _write_settings_file(
        tmp_path,
        """
        service_name: sgcc-audit-backend
        environment: development
        mcp_client:
          command: uv run python rag-server/scripts/run_mcp_server.py
          timeout_seconds: 30
        llm:
          provider: qwen
          model: qwen-plus
        """,
    )

    with pytest.raises(ValidationError):
        load_settings(config_path)
