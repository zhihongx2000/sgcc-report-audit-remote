"""Factory for creating Reranker instances from configuration."""

from __future__ import annotations

from core.settings import RerankSettings
from libs.llm.base_llm import BaseLLM
from rerank.base_reranker import BaseReranker
from rerank.cross_encoder_reranker import CrossEncoderReranker
from rerank.llm_reranker import LLMReranker
from rerank.none_reranker import NoneReranker


def create_reranker(
    settings: RerankSettings,
    *,
    llm: BaseLLM | None = None,
    cache_folder: str | None = None,
) -> BaseReranker:
    """Instantiate a Reranker from *settings*.

    Args:
        settings: Reranker settings section from the application config.
        llm: Required when ``settings.backend == "llm"``; ignored otherwise.
        cache_folder: Optional local model cache directory forwarded to
            :class:`CrossEncoderReranker`.

    Returns:
        A concrete :class:`BaseReranker` instance.

    Raises:
        ValueError: If *settings.backend* is not a registered backend, or if
            ``backend == "llm"`` and *llm* is ``None``.
    """
    backend = settings.backend.lower().strip()

    if backend == "none":
        return NoneReranker()
    if backend == "cross_encoder":
        return CrossEncoderReranker(
            model_name=settings.model,
            max_candidates=settings.max_candidates,
            timeout_sec=settings.timeout_sec,
            cache_folder=cache_folder,
        )
    if backend == "llm":
        if llm is None:
            raise ValueError(
                "'llm' must be provided when reranker backend is 'llm'."
            )
        return LLMReranker(
            llm=llm,
            max_candidates=settings.max_candidates,
        )
    raise ValueError(
        f"Unknown reranker backend '{settings.backend}'. "
        "Available backends: cross_encoder, llm, none"
    )
