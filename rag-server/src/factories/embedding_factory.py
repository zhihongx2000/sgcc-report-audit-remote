"""Factory for creating Embedding instances from configuration."""

from __future__ import annotations

from libs.embedding.base_embedding import BaseEmbedding
from libs.embedding.bge_embedding import BGEEmbedding
from libs.embedding.ollama_embedding import OllamaEmbedding
from libs.embedding.openai_embedding import OpenAIEmbedding


def create_embedding(provider: str, **kwargs) -> BaseEmbedding:  # noqa: ANN003
    """Instantiate an Embedding provider by *provider* name.

    Args:
        provider: Embedding provider identifier (``"openai"``, ``"bge"``,
            ``"ollama"``).  
        **kwargs: Provider-specific keyword arguments forwarded to the
            constructor.  Required kwargs per provider:
            - ``openai``: ``api_key``, ``model``.
            - ``bge``: ``model_name_or_path`` (optional, has default).
            - ``ollama``: ``model``.

    Returns:
        A concrete :class:`BaseEmbedding` instance.

    Raises:
        ValueError: If *provider* is not a registered provider.
        KeyError: If a required provider-specific kwarg is missing.
    """
    _provider = provider.lower().strip()

    if _provider == "openai":
        return OpenAIEmbedding(
            api_key=kwargs["api_key"],
            model=kwargs["model"],
            timeout_seconds=float(kwargs.get("timeout_seconds", 60.0)),
            base_url=kwargs.get("base_url"),
        )
    if _provider == "bge":
        return BGEEmbedding(
            model_name_or_path=kwargs.get(
                "model_name_or_path", "BAAI/bge-large-zh-v1.5"
            ),
            device=kwargs.get("device"),
            batch_size=int(kwargs.get("batch_size", 32)),
            normalize_embeddings=bool(
                kwargs.get("normalize_embeddings", True)),
            cache_folder=kwargs.get("cache_folder"),
        )
    if _provider == "ollama":
        return OllamaEmbedding(
            model=kwargs["model"],
            base_url=kwargs.get("base_url", "http://localhost:11434"),
            timeout_seconds=float(kwargs.get("timeout_seconds", 60.0)),
        )
    raise ValueError(
        f"Unknown embedding provider '{provider}'. "
        "Available providers: bge, ollama, openai"
    )
