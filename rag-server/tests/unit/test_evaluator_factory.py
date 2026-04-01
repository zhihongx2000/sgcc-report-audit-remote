"""Unit tests for D8: Evaluator abstraction and factory placeholder.

Coverage:
- BaseEvaluator / EvalInput / EvalResult: correct construction and field defaults
- _NoneEvaluator: returns EvalResult with empty metrics dict
- create_evaluator: routes to correct backend, raises ValueError for unknown types
"""

from __future__ import annotations

import pytest

from evaluation.base_evaluator import BaseEvaluator, EvalInput, EvalResult
from factories.evaluator_factory import create_evaluator


# ---------------------------------------------------------------------------
# EvalInput / EvalResult dataclass tests
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEvalDataclasses:
    def test_eval_input_required_fields(self) -> None:
        inp = EvalInput(
            query="test query",
            retrieved_chunks=["chunk1", "chunk2"],
            generated_answer="answer",
        )
        assert inp.query == "test query"
        assert inp.retrieved_chunks == ["chunk1", "chunk2"]
        assert inp.generated_answer == "answer"
        assert inp.ground_truth == ""
        assert inp.metadata == {}

    def test_eval_input_optional_fields(self) -> None:
        inp = EvalInput(
            query="q",
            retrieved_chunks=[],
            generated_answer="a",
            ground_truth="ref",
            metadata={"source": "test"},
        )
        assert inp.ground_truth == "ref"
        assert inp.metadata["source"] == "test"

    def test_eval_result_defaults(self) -> None:
        result = EvalResult()
        assert result.metrics == {}
        assert result.metadata == {}

    def test_eval_result_with_metrics(self) -> None:
        result = EvalResult(metrics={"hit_rate": 0.8, "faithfulness": 0.9})
        assert result.metrics["hit_rate"] == pytest.approx(0.8)
        assert result.metrics["faithfulness"] == pytest.approx(0.9)


# ---------------------------------------------------------------------------
# BaseEvaluator is abstract
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestBaseEvaluatorAbstract:
    def test_cannot_instantiate_base_evaluator(self) -> None:
        with pytest.raises(TypeError):
            BaseEvaluator()  # type: ignore[abstract]


# ---------------------------------------------------------------------------
# NoneEvaluator (placeholder backend)
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestNoneEvaluator:
    def setup_method(self) -> None:
        self.evaluator = create_evaluator("none")

    def test_returns_eval_result(self) -> None:
        inp = EvalInput(query="q", retrieved_chunks=[
                        "c1"], generated_answer="a")
        result = self.evaluator.evaluate(inp)
        assert isinstance(result, EvalResult)

    def test_returns_empty_metrics(self) -> None:
        inp = EvalInput(query="q", retrieved_chunks=[], generated_answer="a")
        result = self.evaluator.evaluate(inp)
        assert result.metrics == {}

    def test_metadata_contains_backend_name(self) -> None:
        inp = EvalInput(query="q", retrieved_chunks=[], generated_answer="a")
        result = self.evaluator.evaluate(inp)
        assert result.metadata.get("backend") == "none"


# ---------------------------------------------------------------------------
# Factory routing
# ---------------------------------------------------------------------------

@pytest.mark.unit
class TestEvaluatorFactory:
    def test_create_none_evaluator(self) -> None:
        evaluator = create_evaluator("none")
        assert isinstance(evaluator, BaseEvaluator)

    def test_create_none_evaluator_case_insensitive(self) -> None:
        evaluator = create_evaluator("None")
        assert isinstance(evaluator, BaseEvaluator)

    def test_unknown_backend_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown evaluator backend"):
            create_evaluator("ragas")

    def test_unknown_backend_message_includes_available_backends(self) -> None:
        with pytest.raises(ValueError, match="none"):
            create_evaluator("unsupported_backend")

    def test_empty_backend_raises_value_error(self) -> None:
        with pytest.raises(ValueError, match="Unknown evaluator backend"):
            create_evaluator("")
