"""Unit tests for D9: full factory routing across all component factories.

Coverage:
- LLM factory: all 6 providers routed correctly; unknown provider raises ValueError
- Vision LLM factory: azure/qwen routed; unknown provider raises ValueError
- Embedding factory: openai/bge/ollama routed; unknown provider raises ValueError
- Splitter factory: recursive_character/parent_child routed; unknown raises ValueError
- VectorStore factory: pgvector routed; unknown backend raises ValueError
- Reranker factory: none/cross_encoder/llm routed; llm without llm-arg raises ValueError

All external provider classes are mocked to avoid real API calls or model loads.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from core.settings import LLMSettings, RerankSettings, VectorStoreSettings
from factories.embedding_factory import create_embedding
from factories.llm_factory import create_llm
from factories.reranker_factory import create_reranker
from factories.splitter_factory import create_splitter
from factories.vector_store_factory import create_vector_store
from factories.vision_llm_factory import create_vision_llm
from ingestion.splitters.parent_child_splitter import ParentChildSplitter
from ingestion.splitters.recursive_character_splitter import (
    RecursiveCharacterSplitter,
)
from rerank.none_reranker import NoneReranker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _llm_settings(provider: str = "openai") -> LLMSettings:
    return LLMSettings(provider=provider, model="test-model", api_key="test-key")


# ---------------------------------------------------------------------------
# LLM Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestLLMFactory:
    @pytest.mark.parametrize("provider,cls_path", [
        ("openai", "factories.llm_factory.OpenAILLM"),
        ("qwen", "factories.llm_factory.QwenLLM"),
        ("deepseek", "factories.llm_factory.DeepSeekLLM"),
    ])
    def test_simple_providers_routed(self, provider: str, cls_path: str) -> None:
        with patch(cls_path) as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_llm(_llm_settings(provider))
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_azure_provider_routed(self) -> None:
        with patch("factories.llm_factory.AzureOpenAILLM") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_llm(
                _llm_settings("azure"),
                endpoint="https://test.openai.azure.com",
                api_version="2024-02-01",
                deployment_name="gpt-4o",
            )
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_vllm_provider_routed(self) -> None:
        with patch("factories.llm_factory.VLLMLLM") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_llm(
                _llm_settings("vllm"),
                base_url="http://localhost:8000/v1",
            )
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_ollama_provider_routed(self) -> None:
        with patch("factories.llm_factory.OllamaLLM") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_llm(_llm_settings("ollama"))
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_unknown_provider_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown LLM provider"):
            create_llm(_llm_settings("unsupported"))

    def test_provider_name_case_insensitive(self) -> None:
        with patch("factories.llm_factory.QwenLLM") as mock_cls:
            mock_cls.return_value = MagicMock()
            create_llm(_llm_settings("QWEN"))
            mock_cls.assert_called_once()


# ---------------------------------------------------------------------------
# Vision LLM Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestVisionLLMFactory:
    @pytest.mark.parametrize("provider,cls_path,kwargs", [
        (
            "azure",
            "factories.vision_llm_factory.AzureVisionLLM",
            {
                "endpoint": "https://test.openai.azure.com",
                "api_key": "key",
                "api_version": "2024-02-01",
                "deployment_name": "gpt-4o",
            },
        ),
        (
            "qwen",
            "factories.vision_llm_factory.QwenVLClient",
            {"api_key": "key", "model": "qwen-vl-plus"},
        ),
    ])
    def test_providers_routed(
        self, provider: str, cls_path: str, kwargs: dict
    ) -> None:
        with patch(cls_path) as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_vision_llm(provider, **kwargs)
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_unknown_provider_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown Vision LLM provider"):
            create_vision_llm("unsupported", api_key="x", model="y")


# ---------------------------------------------------------------------------
# Embedding Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEmbeddingFactory:
    @pytest.mark.parametrize("provider,cls_path,kwargs", [
        (
            "openai",
            "factories.embedding_factory.OpenAIEmbedding",
            {"api_key": "key", "model": "text-embedding-3-small"},
        ),
        (
            "bge",
            "factories.embedding_factory.BGEEmbedding",
            {"model_name_or_path": "BAAI/bge-large-zh-v1.5"},
        ),
        (
            "ollama",
            "factories.embedding_factory.OllamaEmbedding",
            {"model": "nomic-embed-text"},
        ),
    ])
    def test_providers_routed(
        self, provider: str, cls_path: str, kwargs: dict
    ) -> None:
        with patch(cls_path) as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_embedding(provider, **kwargs)
            mock_cls.assert_called_once()
            assert result is mock_cls.return_value

    def test_bge_uses_default_model(self) -> None:
        with patch("factories.embedding_factory.BGEEmbedding") as mock_cls:
            mock_cls.return_value = MagicMock()
            create_embedding("bge")
            call_kwargs = mock_cls.call_args[1]
            assert call_kwargs["model_name_or_path"] == "BAAI/bge-large-zh-v1.5"

    def test_unknown_provider_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown embedding provider"):
            create_embedding("unsupported")


# ---------------------------------------------------------------------------
# Splitter Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSplitterFactory:
    def test_recursive_character_type(self) -> None:
        splitter = create_splitter("recursive_character")
        assert isinstance(splitter, RecursiveCharacterSplitter)

    def test_parent_child_type(self) -> None:
        splitter = create_splitter("parent_child")
        assert isinstance(splitter, ParentChildSplitter)

    def test_recursive_character_kwargs(self) -> None:
        splitter = create_splitter(
            "recursive_character", chunk_size=500, chunk_overlap=50
        )
        assert isinstance(splitter, RecursiveCharacterSplitter)
        assert splitter._chunk_size == 500
        assert splitter._chunk_overlap == 50

    def test_parent_child_kwargs(self) -> None:
        splitter = create_splitter(
            "parent_child", parent_chunk_size=3000, child_chunk_size=600
        )
        assert isinstance(splitter, ParentChildSplitter)
        assert splitter._parent_chunk_size == 3000
        assert splitter._child_chunk_size == 600

    def test_unknown_type_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown splitter type"):
            create_splitter("unsupported")


# ---------------------------------------------------------------------------
# VectorStore Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestVectorStoreFactory:
    def _settings(self, backend: str = "pgvector") -> VectorStoreSettings:
        return VectorStoreSettings(
            backend=backend,
            table="rag_chunks",
            embedding_dim=1024,
            distance_metric="cosine",
        )

    def test_pgvector_backend_routed(self) -> None:
        mock_engine = MagicMock()
        with patch("factories.vector_store_factory.PgVectorStore") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_vector_store(
                self._settings("pgvector"), engine=mock_engine)
            mock_cls.assert_called_once_with(
                mock_engine,
                table="rag_chunks",
                embedding_dim=1024,
                distance_metric="cosine",
            )
            assert result is mock_cls.return_value

    def test_unknown_backend_raises_value_error(self) -> None:
        mock_engine = MagicMock()
        with pytest.raises(ValueError, match="Unknown vector store backend"):
            create_vector_store(self._settings(
                "unsupported"), engine=mock_engine)


# ---------------------------------------------------------------------------
# Reranker Factory
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestRerankerFactory:
    def _settings(self, backend: str) -> RerankSettings:
        return RerankSettings(
            backend=backend,
            model="BAAI/bge-reranker-v2-m3",
            max_candidates=30,
            timeout_sec=10.0,
            fallback_to_none=True,
        )

    def test_none_backend(self) -> None:
        reranker = create_reranker(self._settings("none"))
        assert isinstance(reranker, NoneReranker)

    def test_cross_encoder_backend(self) -> None:
        with patch("factories.reranker_factory.CrossEncoderReranker") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_reranker(self._settings("cross_encoder"))
            mock_cls.assert_called_once_with(
                model_name="BAAI/bge-reranker-v2-m3",
                max_candidates=30,
                timeout_sec=10.0,
                cache_folder=None,
            )
            assert result is mock_cls.return_value

    def test_llm_backend_requires_llm(self) -> None:
        with pytest.raises(ValueError, match="'llm' must be provided"):
            create_reranker(self._settings("llm"), llm=None)

    def test_llm_backend_with_llm(self) -> None:
        mock_llm = MagicMock()
        with patch("factories.reranker_factory.LLMReranker") as mock_cls:
            mock_cls.return_value = MagicMock()
            result = create_reranker(self._settings("llm"), llm=mock_llm)
            mock_cls.assert_called_once_with(llm=mock_llm, max_candidates=30)
            assert result is mock_cls.return_value

    def test_unknown_backend_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown reranker backend"):
            create_reranker(self._settings("unsupported"))
