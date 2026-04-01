"""D10: validate_settings() unit tests.

Covers:
- Invalid config samples (placeholder api_key, azure missing endpoint, dim mismatch,
  final_top_k > dense_top_k)
- Valid config regression (default settings.yaml loads without semantic errors)
"""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from core.settings import (
    EmbeddingSettings,
    LLMSettings,
    RerankSettings,
    RetrievalSettings,
    Settings,
    VectorStoreSettings,
    load_settings,
    validate_settings,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _minimal_settings(**overrides) -> Settings:
    """Build a minimal valid Settings object, applying keyword overrides."""
    base = {
        "llm": {"provider": "qwen", "model": "qwen-plus", "api_key": "real-key"},
    }
    base.update(overrides)
    return Settings.model_validate(base)


# ---------------------------------------------------------------------------
# validate_settings: invalid samples
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValidateSettingsInvalid:
    def test_placeholder_api_key_reported(self) -> None:
        settings = _minimal_settings(
            llm={"provider": "qwen", "model": "qwen-plus", "api_key": "replace-me"}
        )
        errors = validate_settings(settings)
        assert any(
            "api_key" in e for e in errors), f"Expected api_key error in {errors}"

    def test_azure_requires_endpoint(self) -> None:
        settings = _minimal_settings(
            llm={
                "provider": "azure",
                "model": "gpt-4o",
                "api_key": "real-key",
                # No endpoint or deployment_name
            }
        )
        errors = validate_settings(settings)
        assert any("endpoint" in e for e in errors)
        assert any("deployment_name" in e for e in errors)

    def test_azure_requires_deployment_name(self) -> None:
        settings = _minimal_settings(
            llm={
                "provider": "azure",
                "model": "gpt-4o",
                "api_key": "real-key",
                "endpoint": "https://example.openai.azure.com",
                # missing deployment_name
            }
        )
        errors = validate_settings(settings)
        assert any("deployment_name" in e for e in errors)
        # endpoint is provided, so no endpoint error
        assert not any("endpoint" in e and "required" in e for e in errors)

    def test_embedding_dim_mismatch_reported(self) -> None:
        settings = _minimal_settings(
            embedding={"provider": "bge",
                       "model": "BAAI/bge-large-zh-v1.5", "embedding_dim": 1024},
            vector_store={
                "backend": "pgvector",
                "table": "rag_chunks",
                "embedding_dim": 1536,  # mismatch
            },
        )
        errors = validate_settings(settings)
        assert any("embedding_dim" in e and "mismatch" in e for e in errors)

    def test_final_top_k_exceeds_dense_top_k(self) -> None:
        settings = _minimal_settings(
            retrieval={
                "top_k": 5,
                "dense_top_k": 10,
                "final_top_k": 20,  # exceeds dense_top_k
            }
        )
        errors = validate_settings(settings)
        assert any("final_top_k" in e for e in errors)


# ---------------------------------------------------------------------------
# validate_settings: valid config regression
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestValidateSettingsValid:
    def test_default_settings_yaml_has_no_semantic_errors(self) -> None:
        """The default settings.yaml should load and produce no validate_settings errors
        except the expected placeholder api_key warning (which is intentional for dev)."""
        settings = load_settings()
        errors = validate_settings(settings)
        # The only expected error is the placeholder api_key warning
        semantic_errors = [e for e in errors if "api_key" not in e]
        assert semantic_errors == [], (
            f"Unexpected semantic errors in default settings.yaml: {semantic_errors}"
        )

    def test_fully_valid_config_returns_no_errors(self) -> None:
        settings = _minimal_settings(
            llm={"provider": "qwen", "model": "qwen-plus", "api_key": "real-key"},
            embedding={"provider": "bge",
                       "model": "BAAI/bge-large-zh-v1.5", "embedding_dim": 1024},
            vector_store={
                "backend": "pgvector",
                "table": "rag_chunks",
                "embedding_dim": 1024,
            },
            retrieval={
                "top_k": 5,
                "dense_top_k": 30,
                "final_top_k": 10,
            },
        )
        errors = validate_settings(settings)
        assert errors == []

    def test_azure_valid_config_returns_no_errors(self) -> None:
        settings = _minimal_settings(
            llm={
                "provider": "azure",
                "model": "gpt-4o",
                "api_key": "real-key",
                "endpoint": "https://example.openai.azure.com",
                "deployment_name": "gpt-4o",
                "api_version": "2024-10-21",
            },
            # embedding_dim must match vector_store to avoid dim-mismatch error
            embedding={"provider": "bge",
                       "model": "BAAI/bge-large-zh-v1.5", "embedding_dim": 1024},
            vector_store={"backend": "pgvector",
                          "table": "rag_chunks", "embedding_dim": 1024},
        )
        errors = validate_settings(settings)
        assert errors == []


# ---------------------------------------------------------------------------
# Pydantic model structural validation
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestSettingsModelValidation:
    def test_llm_missing_provider_raises(self) -> None:
        with pytest.raises(ValidationError):
            LLMSettings(model="gpt-4", api_key="k")  # provider missing

    def test_llm_empty_api_key_raises(self) -> None:
        with pytest.raises(ValidationError):
            LLMSettings(provider="openai", model="gpt-4", api_key="")

    def test_rerank_negative_timeout_raises(self) -> None:
        with pytest.raises(ValidationError):
            RerankSettings(backend="none", model="m",
                           max_candidates=10, timeout_sec=-1.0)

    def test_splitter_overlap_gte_chunk_size_raises(self) -> None:
        from core.settings import SplitterSettings

        with pytest.raises(ValidationError):
            SplitterSettings(chunk_size=100, chunk_overlap=100)

    def test_retrieval_top_k_ge_1(self) -> None:
        with pytest.raises(ValidationError):
            RetrievalSettings(top_k=0)

    def test_full_settings_all_sections_loaded(self) -> None:
        settings = load_settings()
        assert settings.app is not None
        assert settings.embedding is not None
        assert settings.vision_llm is not None
        assert settings.splitter is not None
        assert settings.evaluation is not None
        assert settings.observability is not None
        assert settings.mcp is not None
        assert settings.paths is not None
        assert settings.loader is not None
