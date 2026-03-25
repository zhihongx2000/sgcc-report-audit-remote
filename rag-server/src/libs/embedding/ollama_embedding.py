"""Ollama local Embedding provider adapter using the native ollama SDK."""

from __future__ import annotations

import ollama as _ollama

from libs.embedding.base_embedding import BaseEmbedding
from utils.retry import RetryPolicy


class OllamaEmbedding(BaseEmbedding):
	"""Embedding adapter for locally hosted Ollama server."""

	def __init__(
		self,
		*,
		model: str,
		base_url: str = "http://localhost:11434",
		timeout_seconds: float = 60.0,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._client = _ollama.Client(host=base_url, timeout=timeout_seconds)
		self._model = model

	def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
		response = self._client.embed(model=self._model, input=texts)
		return [list(v) for v in response.embeddings]
