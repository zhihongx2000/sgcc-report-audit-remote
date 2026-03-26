"""CrossEncoderReranker – reranker backed by a sentence-transformers CrossEncoder.

The model scores each ``[query, chunk_text]`` pair and returns candidates
sorted by their predicted relevance scores.  On timeout or any failure the
implementation falls back to ``NoneReranker`` (fusion ordering preserved).
"""

from __future__ import annotations

import concurrent.futures
import logging
from typing import Any

from rerank.base_reranker import BaseReranker, RerankCandidate
from rerank.none_reranker import NoneReranker

logger = logging.getLogger(__name__)


class CrossEncoderReranker(BaseReranker):
	"""Reranker using a local/hosted Cross-Encoder model via sentence-transformers.

	Scores each ``(query, chunk_text)`` pair and returns results sorted by
	descending relevance score.  Falls back to fusion ordering on timeout or
	model failure.

	Args:
		model_name: Sentence-transformers model identifier
			(e.g. ``"BAAI/bge-reranker-v2-m3"``).
		max_candidates: Maximum number of candidates to pass to the model;
			recommended ``10–30`` for CPU environments.
		timeout_sec: Maximum wall-clock seconds to wait for model inference.
	"""

	def __init__(
		self,
		model_name: str = "BAAI/bge-reranker-v2-m3",
		*,
		max_candidates: int = 30,
		timeout_sec: float = 10.0,
		cache_folder: str | None = None,
	) -> None:
		self._model_name = model_name
		self._max_candidates = max_candidates
		self._timeout_sec = timeout_sec
		self._cache_folder = cache_folder  # e.g. "rag-server/models"
		self._fallback = NoneReranker()
		self._model: Any = None  # lazy-loaded on first rerank call

	def _load_model(self) -> Any:
		"""Lazily load the CrossEncoder model."""
		if self._model is None:
			from sentence_transformers import CrossEncoder  # type: ignore[import-untyped]

			kwargs: dict = {}
			if self._cache_folder is not None:
				kwargs["cache_folder"] = self._cache_folder
			self._model = CrossEncoder(self._model_name, **kwargs)
		return self._model

	def rerank(
		self,
		query: str,
		candidates: list[RerankCandidate],
		*,
		top_k: int = 10,
	) -> list[RerankCandidate]:
		if not candidates:
			return []

		# Limit candidates for CPU performance
		candidates_to_rank = candidates[: self._max_candidates]

		try:
			with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
				future = executor.submit(self._score, query, candidates_to_rank)
				scored = future.result(timeout=self._timeout_sec)
		except concurrent.futures.TimeoutError:
			logger.warning(
				"CrossEncoderReranker timed out after %.1f s (model=%s); "
				"falling back to fusion ordering",
				self._timeout_sec,
				self._model_name,
			)
			return self._fallback.rerank(query, candidates, top_k=top_k)
		except Exception:
			logger.exception(
				"CrossEncoderReranker failed (model=%s); "
				"falling back to fusion ordering",
				self._model_name,
			)
			return self._fallback.rerank(query, candidates, top_k=top_k)

		return scored[:top_k]

	def _score(
		self,
		query: str,
		candidates: list[RerankCandidate],
	) -> list[RerankCandidate]:
		"""Run model inference and return score-sorted candidates."""
		model = self._load_model()
		pairs = [[query, c.text] for c in candidates]
		raw_scores: list[float] = model.predict(pairs).tolist()

		scored = [
			RerankCandidate(
				id=c.id,
				text=c.text,
				score=float(s),
				metadata=c.metadata,
			)
			for c, s in zip(candidates, raw_scores)
		]
		scored.sort(key=lambda x: x.score, reverse=True)
		return scored
