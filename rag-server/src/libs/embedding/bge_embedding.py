"""BGE local Embedding provider adapter using sentence-transformers."""

from __future__ import annotations

from libs.embedding.base_embedding import BaseEmbedding
from utils.retry import RetryPolicy

try:
	import sentence_transformers  # type: ignore[import-untyped]
except ImportError:  # pragma: no cover
	sentence_transformers = None  # type: ignore[assignment]


class BGEEmbedding(BaseEmbedding):
	"""Embedding adapter for BAAI BGE models loaded locally via sentence-transformers.

	The underlying model is loaded lazily on the first call to ``_embed_texts_once``
	to avoid paying the import cost unless this provider is actually used.
	"""

	def __init__(
		self,
		*,
		model_name_or_path: str = "BAAI/bge-large-zh-v1.5",
		device: str | None = None,
		batch_size: int = 32,
		normalize_embeddings: bool = True,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._model_name_or_path = model_name_or_path
		self._device = device
		self._batch_size = batch_size
		self._normalize_embeddings = normalize_embeddings
		self._model = None  # lazy init

	def _load_model(self) -> None:
		"""Load the SentenceTransformer model on first use."""
		if sentence_transformers is None:
			raise ImportError(
				"sentence-transformers is required for BGEEmbedding. "
				"Install it with: uv add sentence-transformers"
			)
		kwargs: dict = {}
		if self._device is not None:
			kwargs["device"] = self._device
		self._model = sentence_transformers.SentenceTransformer(
			self._model_name_or_path, **kwargs
		)

	def _embed_texts_once(self, texts: list[str]) -> list[list[float]]:
		if self._model is None:
			self._load_model()
		vectors = self._model.encode(
			texts,
			batch_size=self._batch_size,
			normalize_embeddings=self._normalize_embeddings,
			convert_to_numpy=True,
		)
		return [v.tolist() for v in vectors]
