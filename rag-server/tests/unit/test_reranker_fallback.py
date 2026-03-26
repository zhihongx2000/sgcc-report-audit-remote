"""Unit tests for D7: Reranker abstraction and three implementations.

Coverage:
- NoneReranker: passthrough ordering, top_k slicing, empty list
- CrossEncoderReranker: score-based sort, timeout fallback, exception fallback
- LLMReranker: ranked_ids parsing, JSON error fallback, LLM exception fallback
- Sort stability: top-scoring candidate is first
"""

from __future__ import annotations

import concurrent.futures
import json
from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from rerank.base_reranker import RerankCandidate
from rerank.cross_encoder_reranker import CrossEncoderReranker
from rerank.llm_reranker import LLMReranker
from rerank.none_reranker import NoneReranker


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_candidates(n: int) -> list[RerankCandidate]:
	"""Build *n* dummy candidates with fusion score == index (ascending)."""
	return [
		RerankCandidate(id=f"id_{i}", text=f"chunk text {i}", score=float(i))
		for i in range(n)
	]


# ---------------------------------------------------------------------------
# NoneReranker
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestNoneReranker:
	def setup_method(self) -> None:
		self.reranker = NoneReranker()

	def test_returns_candidates_in_original_order(self) -> None:
		candidates = make_candidates(5)
		result = self.reranker.rerank("query", candidates, top_k=10)
		assert [c.id for c in result] == [f"id_{i}" for i in range(5)]

	def test_top_k_limits_output(self) -> None:
		candidates = make_candidates(5)
		result = self.reranker.rerank("query", candidates, top_k=3)
		assert len(result) == 3
		assert result[0].id == "id_0"

	def test_empty_candidates_returns_empty(self) -> None:
		result = self.reranker.rerank("query", [], top_k=10)
		assert result == []

	def test_top_k_larger_than_candidates_returns_all(self) -> None:
		candidates = make_candidates(3)
		result = self.reranker.rerank("query", candidates, top_k=100)
		assert len(result) == 3


# ---------------------------------------------------------------------------
# CrossEncoderReranker
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestCrossEncoderReranker:
	def _make_mock_model(self, scores: list[float]) -> MagicMock:
		"""Return a mock CrossEncoder whose predict() returns *scores*."""
		mock_model = MagicMock()
		mock_model.predict.return_value = np.array(scores)
		return mock_model

	def test_sort_by_score_descending(self) -> None:
		"""Model assigns highest score to last candidate; reranker should reorder."""
		candidates = make_candidates(3)  # id_0, id_1, id_2
		# id_2 gets score 0.9, id_0 gets 0.5, id_1 gets 0.3
		mock_model = self._make_mock_model([0.5, 0.3, 0.9])

		reranker = CrossEncoderReranker(model_name="mock-model", timeout_sec=5.0)
		reranker._model = mock_model

		result = reranker.rerank("what is power quality?", candidates, top_k=3)

		assert result[0].id == "id_2"
		assert result[0].score == pytest.approx(0.9)
		assert result[1].id == "id_0"
		assert result[2].id == "id_1"

	def test_top_k_limits_ranked_output(self) -> None:
		candidates = make_candidates(3)
		mock_model = self._make_mock_model([0.5, 0.3, 0.9])

		reranker = CrossEncoderReranker(model_name="mock-model", timeout_sec=5.0)
		reranker._model = mock_model

		result = reranker.rerank("query", candidates, top_k=2)
		assert len(result) == 2
		assert result[0].id == "id_2"

	def test_empty_candidates_returns_empty(self) -> None:
		reranker = CrossEncoderReranker(model_name="mock-model")
		result = reranker.rerank("query", [], top_k=10)
		assert result == []

	def test_fallback_on_timeout(self) -> None:
		"""When model inference times out, result preserves fusion ordering."""
		candidates = make_candidates(4)

		def slow_predict(pairs: list) -> np.ndarray:
			import time
			time.sleep(60)  # simulate hang
			return np.zeros(len(pairs))

		mock_model = MagicMock()
		mock_model.predict.side_effect = slow_predict

		reranker = CrossEncoderReranker(
			model_name="mock-model",
			max_candidates=10,
			timeout_sec=0.05,  # very short timeout
		)
		reranker._model = mock_model

		result = reranker.rerank("query", candidates, top_k=3)
		# Fallback to NoneReranker: original order, top_k=3
		assert [c.id for c in result] == ["id_0", "id_1", "id_2"]

	def test_fallback_on_model_exception(self) -> None:
		"""When model raises an exception, result falls back to fusion ordering."""
		candidates = make_candidates(3)

		mock_model = MagicMock()
		mock_model.predict.side_effect = RuntimeError("model crashed")

		reranker = CrossEncoderReranker(model_name="mock-model", timeout_sec=5.0)
		reranker._model = mock_model

		result = reranker.rerank("query", candidates, top_k=3)
		assert [c.id for c in result] == ["id_0", "id_1", "id_2"]

	def test_max_candidates_limits_model_input(self) -> None:
		"""CrossEncoderReranker should only pass max_candidates to the model."""
		candidates = make_candidates(10)
		# Model returns scores for only first 5 candidates
		mock_model = self._make_mock_model([0.1, 0.2, 0.3, 0.4, 0.5])

		reranker = CrossEncoderReranker(
			model_name="mock-model",
			max_candidates=5,
			timeout_sec=5.0,
		)
		reranker._model = mock_model

		result = reranker.rerank("query", candidates, top_k=5)
		# Only first 5 candidates are scored; scored by model, reversed
		assert len(result) == 5
		assert result[0].id == "id_4"  # highest model score (0.5)


# ---------------------------------------------------------------------------
# LLMReranker
# ---------------------------------------------------------------------------

def _make_llm_mock(response: str) -> MagicMock:
	"""Return a mock BaseLLM whose generate() returns *response*."""
	mock_llm = MagicMock()
	mock_llm.generate.return_value = response
	return mock_llm


@pytest.mark.unit
class TestLLMReranker:
	def test_ranked_ids_reorders_candidates(self) -> None:
		candidates = make_candidates(3)  # id_0, id_1, id_2
		llm_response = json.dumps({"ranked_ids": ["id_2", "id_0", "id_1"]})

		reranker = LLMReranker(_make_llm_mock(llm_response))
		result = reranker.rerank("query", candidates, top_k=3)

		assert [c.id for c in result] == ["id_2", "id_0", "id_1"]

	def test_top_k_limits_llm_output(self) -> None:
		candidates = make_candidates(3)
		llm_response = json.dumps({"ranked_ids": ["id_2", "id_0", "id_1"]})

		reranker = LLMReranker(_make_llm_mock(llm_response))
		result = reranker.rerank("query", candidates, top_k=2)

		assert len(result) == 2
		assert result[0].id == "id_2"

	def test_tolerates_json_with_surrounding_prose(self) -> None:
		"""LLMReranker extracts JSON even when prose surrounds the object."""
		candidates = make_candidates(2)
		llm_response = 'Sure! Here you go: {"ranked_ids": ["id_1", "id_0"]} Done.'

		reranker = LLMReranker(_make_llm_mock(llm_response))
		result = reranker.rerank("query", candidates, top_k=2)

		assert result[0].id == "id_1"
		assert result[1].id == "id_0"

	def test_fallback_on_invalid_json(self) -> None:
		"""Invalid JSON response falls back to fusion ordering."""
		candidates = make_candidates(3)
		reranker = LLMReranker(_make_llm_mock("not a valid json response"))
		result = reranker.rerank("query", candidates, top_k=3)
		assert [c.id for c in result] == ["id_0", "id_1", "id_2"]

	def test_fallback_on_missing_ranked_ids_key(self) -> None:
		"""JSON missing 'ranked_ids' key falls back to fusion ordering."""
		candidates = make_candidates(3)
		llm_response = json.dumps({"result": ["id_1", "id_0"]})
		reranker = LLMReranker(_make_llm_mock(llm_response))
		result = reranker.rerank("query", candidates, top_k=3)
		assert [c.id for c in result] == ["id_0", "id_1", "id_2"]

	def test_fallback_on_llm_exception(self) -> None:
		"""LLM raising an exception falls back to fusion ordering."""
		candidates = make_candidates(3)
		mock_llm = MagicMock()
		mock_llm.generate.side_effect = RuntimeError("LLM unavailable")

		reranker = LLMReranker(mock_llm)
		result = reranker.rerank("query", candidates, top_k=3)
		assert [c.id for c in result] == ["id_0", "id_1", "id_2"]

	def test_empty_candidates_returns_empty(self) -> None:
		reranker = LLMReranker(_make_llm_mock(""))
		result = reranker.rerank("query", [], top_k=10)
		assert result == []

	def test_omitted_candidates_appended_at_end(self) -> None:
		"""Candidates omitted by LLM are appended after ranked ones."""
		candidates = make_candidates(3)  # id_0, id_1, id_2
		# LLM only ranks id_2 and id_0; id_1 is omitted
		llm_response = json.dumps({"ranked_ids": ["id_2", "id_0"]})

		reranker = LLMReranker(_make_llm_mock(llm_response), max_candidates=10)
		result = reranker.rerank("query", candidates, top_k=3)

		assert result[0].id == "id_2"
		assert result[1].id == "id_0"
		assert result[2].id == "id_1"  # omitted by LLM, appended last


# ---------------------------------------------------------------------------
# Sort stability: top-relevance candidate should always come first
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestSortStability:
	def test_cross_encoder_top_candidate_is_first(self) -> None:
		candidates = [
			RerankCandidate(id="a", text="power quality report", score=0.5),
			RerankCandidate(id="b", text="weather forecast", score=0.9),
			RerankCandidate(id="c", text="voltage harmonics", score=0.7),
		]
		mock_model = MagicMock()
		# Assign score 0.99 to candidate "a", lower to others
		mock_model.predict.return_value = np.array([0.99, 0.1, 0.5])

		reranker = CrossEncoderReranker(model_name="mock-model", timeout_sec=5.0)
		reranker._model = mock_model

		result = reranker.rerank("power quality", candidates, top_k=3)
		assert result[0].id == "a"

	def test_llm_reranker_top_candidate_is_first(self) -> None:
		candidates = [
			RerankCandidate(id="x", text="unrelated text", score=0.2),
			RerankCandidate(id="y", text="most relevant", score=0.1),
		]
		llm_response = json.dumps({"ranked_ids": ["y", "x"]})

		reranker = LLMReranker(_make_llm_mock(llm_response))
		result = reranker.rerank("relevant query", candidates, top_k=2)
		assert result[0].id == "y"
