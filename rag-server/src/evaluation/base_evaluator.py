"""Abstract Evaluator interface and shared data types for all evaluator backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvalInput:
    """Input bundle supplied to an evaluator.

    Fields:
            query: The search/retrieval query used to generate the answer.
            retrieved_chunks: Text chunks retrieved from the knowledge base.
            generated_answer: The LLM-generated answer to be evaluated.
            ground_truth: Optional reference answer for comparison-based metrics.
            metadata: Arbitrary extra context passed through to all metrics.
    """

    query: str
    retrieved_chunks: list[str]
    generated_answer: str
    ground_truth: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EvalResult:
    """Standardised output returned by every evaluator backend.

    Fields:
            metrics: Numeric metric values keyed by metric name
                      (e.g. ``{"hit_rate": 0.8, "faithfulness": 0.9}``).
            metadata: Backend-specific auxiliary data (raw scores, debug info, etc.).
    """

    metrics: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseEvaluator(ABC):
    """Abstract interface for all evaluator backends.

    All implementations expose a single ``evaluate()`` method that accepts an
    :class:`EvalInput` and returns a standardised :class:`EvalResult`.
    """

    @abstractmethod
    def evaluate(self, eval_input: EvalInput) -> EvalResult:
        """Evaluate a single query-answer pair and return metrics.

        Args:
                eval_input: Bundle containing query, retrieved context, generated
                            answer, and optional ground truth.

        Returns:
                :class:`EvalResult` containing a ``metrics`` dict and optional
                backend metadata.
        """
