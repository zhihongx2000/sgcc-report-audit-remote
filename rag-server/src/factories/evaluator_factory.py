"""Factory for creating Evaluator instances from configuration.

This is the D8 placeholder implementation.  Concrete backends (ragas,
custom_metrics) are wired in during stage J (J1/J2).
"""

from __future__ import annotations

from evaluation.base_evaluator import BaseEvaluator, EvalInput, EvalResult

# ---------------------------------------------------------------------------
# Placeholder evaluator
# ---------------------------------------------------------------------------


class _NoneEvaluator(BaseEvaluator):
    """Pass-through evaluator that returns an empty metrics dict.

    Used as a safe default when no real evaluation backend is configured.
    """

    def evaluate(self, eval_input: EvalInput) -> EvalResult:  # noqa: ARG002
        return EvalResult(metrics={}, metadata={"backend": "none"})


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

_REGISTRY: dict[str, type[BaseEvaluator]] = {
    "none": _NoneEvaluator,
}


def create_evaluator(backend: str, **kwargs) -> BaseEvaluator:  # noqa: ANN003
    """Instantiate an evaluator by *backend* name.

    Args:
            backend: Evaluator backend identifier (e.g. ``"none"``, ``"ragas"``,
                     ``"custom"``).  Must appear in the internal registry.
            **kwargs: Extra keyword arguments forwarded to the evaluator constructor.

    Returns:
            A concrete :class:`BaseEvaluator` instance.

    Raises:
            ValueError: If *backend* is not a registered evaluator type.
    """
    backend = backend.lower().strip()
    if backend not in _REGISTRY:
        raise ValueError(
            f"Unknown evaluator backend '{backend}'. "
            f"Available backends: {sorted(_REGISTRY)}"
        )
    evaluator_cls = _REGISTRY[backend]
    return evaluator_cls(**kwargs)
