"""LLMReranker – reranker that uses an LLM to rank candidates by relevance.

The LLM is prompted to return a JSON object ``{"ranked_ids": [...]}``.  On
any failure (invalid JSON, missing key, LLM exception) the implementation
falls back to ``NoneReranker`` (fusion ordering preserved).
"""

from __future__ import annotations

import json
import logging

from libs.llm.base_llm import BaseLLM
from rerank.base_reranker import BaseReranker, RerankCandidate
from rerank.none_reranker import NoneReranker

logger = logging.getLogger(__name__)

_RANK_PROMPT_TEMPLATE = """\
You are a relevance ranking assistant.

Given a search query and a list of text candidates, rank them by relevance to the query.

Query: {query}

Candidates:
{candidates_text}

Return ONLY a JSON object with a single key "ranked_ids" containing the candidate IDs \
in order of relevance (most relevant first).
Example: {{"ranked_ids": ["id_1", "id_3", "id_2"]}}

Important:
- Include all provided IDs in your response.
- Return ONLY the JSON object, no other text.
"""


class LLMReranker(BaseReranker):
	"""Reranker that uses an LLM to rank candidates by relevance.

	The LLM is asked to return a ``{"ranked_ids": [...]}`` JSON object.  Any
	failure (LLM error, JSON parse failure, missing key) triggers a fallback to
	``NoneReranker`` (fusion ordering preserved).

	Args:
		llm: An instantiated :class:`BaseLLM` implementation.
		max_candidates: Maximum number of candidates to pass to the LLM;
			recommended ``<= 20`` to control cost and latency.
	"""

	def __init__(
		self,
		llm: BaseLLM,
		*,
		max_candidates: int = 20,
	) -> None:
		self._llm = llm
		self._max_candidates = max_candidates
		self._fallback = NoneReranker()

	def rerank(
		self,
		query: str,
		candidates: list[RerankCandidate],
		*,
		top_k: int = 10,
	) -> list[RerankCandidate]:
		if not candidates:
			return []

		candidates_to_rank = candidates[: self._max_candidates]

		try:
			ranked = self._rank_with_llm(query, candidates_to_rank)
		except Exception:
			logger.exception(
				"LLMReranker failed; falling back to fusion ordering"
			)
			return self._fallback.rerank(query, candidates, top_k=top_k)

		# Append any candidates the LLM omitted so nothing is lost
		ranked_ids = {c.id for c in ranked}
		remaining = [c for c in candidates_to_rank if c.id not in ranked_ids]
		full_result = ranked + remaining
		return full_result[:top_k]

	def _rank_with_llm(
		self,
		query: str,
		candidates: list[RerankCandidate],
	) -> list[RerankCandidate]:
		"""Call the LLM and decode the ranked-IDs response."""
		candidates_text = "\n".join(
			f"ID: {c.id}\nText: {c.text[:500]}"  # truncate to keep prompt bounded
			for c in candidates
		)
		prompt = _RANK_PROMPT_TEMPLATE.format(
			query=query,
			candidates_text=candidates_text,
		)

		response = self._llm.generate(prompt)

		# Tolerate surrounding prose around the JSON object
		json_start = response.find("{")
		json_end = response.rfind("}") + 1
		if json_start == -1 or json_end == 0:
			raise ValueError(
				f"LLM response contains no JSON object: {response!r}"
			)

		data: dict[str, list[str]] = json.loads(response[json_start:json_end])
		ranked_ids: list[str] = data["ranked_ids"]

		id_to_candidate = {c.id: c for c in candidates}
		return [
			id_to_candidate[cid]
			for cid in ranked_ids
			if cid in id_to_candidate
		]
