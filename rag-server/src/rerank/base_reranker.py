"""Abstract Reranker interface and shared data types for all reranker backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RerankCandidate:
	"""A candidate chunk supplied to the reranker.

	Fields:
		id: unique chunk/document identifier.
		text: chunk text used for relevance scoring.
		score: upstream fusion score (e.g. from RRF); used as fallback order key.
		metadata: arbitrary key-value metadata preserved across reranking.
	"""

	id: str
	text: str
	score: float
	metadata: dict[str, Any] = field(default_factory=dict)


class BaseReranker(ABC):
	"""Abstract interface for all reranker backends.

	All implementations expose a single ``rerank()`` method.  When the selected
	backend is unavailable or times out, implementations fall back to
	``NoneReranker`` behaviour (preserve upstream ordering).
	"""

	@abstractmethod
	def rerank(
		self,
		query: str,
		candidates: list[RerankCandidate],
		*,
		top_k: int = 10,
	) -> list[RerankCandidate]:
		"""Rerank *candidates* for *query* and return the top *top_k* results.

		Args:
			query: The search query string.
			candidates: Upstream candidates to rerank (e.g. after RRF fusion).
			top_k: Maximum number of results to return.

		Returns:
			Reranked subset of candidates (at most *top_k*), ordered by
			descending relevance.
		"""
