from __future__ import annotations

import textwrap

import pytest
from pydantic import ValidationError

from core.settings import Settings, load_settings


def _write_settings_file(tmp_path, content: str):
    config_path = tmp_path / "settings.yaml"
    config_path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
    return config_path


@pytest.mark.unit
def test_load_settings_uses_default_file() -> None:
    settings = load_settings()

    assert isinstance(settings, Settings)
    assert settings.app_name == "rag-mcp-server"
    assert settings.llm.provider == "qwen"


@pytest.mark.unit
def test_load_settings_env_overrides_key_fields(monkeypatch, tmp_path) -> None:
    config_path = _write_settings_file(
        tmp_path,
        """
        app_name: rag-mcp-server
        environment: development
        llm:
          provider: local
          model: local-model
          api_key: local-key
          timeout_seconds: 20
        retrieval:
          top_k: 3
        """,
    )

    monkeypatch.setenv("RAG_LLM_PROVIDER", "openai")
    monkeypatch.setenv("RAG_LLM_TIMEOUT_SECONDS", "45")

    settings = load_settings(config_path)

    assert settings.llm.provider == "openai"
    assert settings.llm.timeout_seconds == 45
    assert settings.llm.model == "local-model"


@pytest.mark.unit
def test_load_settings_missing_required_field_raises(tmp_path) -> None:
    config_path = _write_settings_file(
        tmp_path,
        """
        app_name: rag-mcp-server
        environment: development
        llm:
          provider: qwen
          model: qwen-plus
        """,
    )

    with pytest.raises(ValidationError):
        load_settings(config_path)
