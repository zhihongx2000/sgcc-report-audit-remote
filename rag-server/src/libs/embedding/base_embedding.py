"""Unified Embedding abstraction used by provider adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from utils.retry import RetryPolicy, retry_call


class BaseEmbedding(ABC):
	"""Base contract for all Embedding providers.

	Provider implementations only need to implement ``_embed_texts_once``.
	Retry behavior is centralized at this layer.
	"""

	def __init__(self, *, retry_policy: RetryPolicy | None = None) -> None:
		self._retry_policy = retry_policy or RetryPolicy()

	@property
	def retry_policy(self) -> RetryPolicy:
		return self._retry_policy

	def embed_texts(self, texts: Sequence[str]) -> list[list[float]]:
		"""Encode a batch of texts into dense vectors with retry.

		Args:
			texts: Non-empty sequence of strings to embed.

		Returns:
			List of float vectors; one vector per input text.

		Raises:
			ValueError: If ``texts`` is empty.
		"""
		if not texts:
			raise ValueError("texts must not be empty")

		return retry_call(
			lambda: self._embed_texts_once(list(texts)),
			policy=self._retry_policy,
		)

	def embed(self, text: str) -> list[float]:
		"""Convenience wrapper: encode a single text into a dense vector."""
		if not text:
			raise ValueError("text must not be empty")
		return self.embed_texts([text])[0]

	@abstractmethod
	def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
		"""Provider-specific single-shot batch embedding (no retry)."""
