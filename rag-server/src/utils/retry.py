"""Lightweight retry helpers used by provider adapters and pipeline calls."""

from __future__ import annotations

from dataclasses import dataclass
from time import sleep
from typing import Callable, TypeVar


T = TypeVar("T")


@dataclass(slots=True)
class RetryPolicy:
	"""Retry policy with deterministic exponential backoff."""

	max_attempts: int = 3
	base_delay_seconds: float = 0.1
	max_delay_seconds: float = 1.0
	backoff_multiplier: float = 2.0
	retry_exceptions: tuple[type[Exception], ...] = (Exception,)

	def __post_init__(self) -> None:
		if self.max_attempts < 1:
			raise ValueError("max_attempts must be >= 1")
		if self.base_delay_seconds < 0:
			raise ValueError("base_delay_seconds must be >= 0")
		if self.max_delay_seconds < 0:
			raise ValueError("max_delay_seconds must be >= 0")
		if self.backoff_multiplier < 1:
			raise ValueError("backoff_multiplier must be >= 1")


def retry_call(
	operation: Callable[[], T],
	*,
	policy: RetryPolicy | None = None,
	sleep_fn: Callable[[float], None] = sleep,
) -> T:
	"""Execute an operation with retry and exponential backoff."""

	resolved_policy = policy or RetryPolicy()
	last_exception: Exception | None = None

	for attempt in range(1, resolved_policy.max_attempts + 1):
		try:
			return operation()
		except resolved_policy.retry_exceptions as exc:  # type: ignore[misc]
			last_exception = exc
			if attempt == resolved_policy.max_attempts:
				raise

			delay = min(
				resolved_policy.base_delay_seconds
				* (resolved_policy.backoff_multiplier ** (attempt - 1)),
				resolved_policy.max_delay_seconds,
			)
			if delay > 0:
				sleep_fn(delay)

	if last_exception is not None:
		raise last_exception

	raise RuntimeError("retry_call reached an unexpected state")
