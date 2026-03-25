"""OpenAI Embedding provider adapter."""

from __future__ import annotations

import openai

from libs.embedding.base_embedding import BaseEmbedding
from utils.retry import RetryPolicy


class OpenAIEmbedding(BaseEmbedding):
	"""Embedding adapter for the OpenAI (and OpenAI-compatible) Embedding API."""

	def __init__(
		self,
		*,
		api_key: str,
		model: str,
		timeout_seconds: float = 60.0,
		base_url: str | None = None,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		client_kwargs: dict = {"api_key": api_key, "timeout": timeout_seconds}
		if base_url is not None:
			client_kwargs["base_url"] = base_url
		self._client = openai.OpenAI(**client_kwargs)
		self._model = model

	def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
		response = self._client.embeddings.create(input=texts, model=self._model)
		# API returns embeddings sorted by index; preserve order explicitly.
		sorted_data = sorted(response.data, key=lambda d: d.index)
		return [d.embedding for d in sorted_data]
