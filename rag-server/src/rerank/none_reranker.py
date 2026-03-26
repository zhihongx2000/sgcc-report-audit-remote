"""NoneReranker – passthrough reranker that preserves upstream fusion ordering."""

from __future__ import annotations

from rerank.base_reranker import BaseReranker, RerankCandidate


class NoneReranker(BaseReranker):
	"""Passthrough reranker that returns candidates in their original order.

	Used as the default strategy when no reranking backend is configured, and
	as the fallback target when a backend fails or times out.
	"""

	def rerank(
		self,
		query: str,
		candidates: list[RerankCandidate],
		*,
		top_k: int = 10,
	) -> list[RerankCandidate]:
		return candidates[:top_k]
