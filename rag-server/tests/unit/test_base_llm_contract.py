from __future__ import annotations

import pytest

from libs.llm.base_llm import BaseLLM, ChatMessage
from utils.retry import RetryPolicy, retry_call


class _RetryableError(RuntimeError):
	pass


class FakeLLM(BaseLLM):
	def __init__(
		self,
		*,
		retry_policy: RetryPolicy | None = None,
		fail_generate_times: int = 0,
		fail_chat_times: int = 0,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._remaining_generate_failures = fail_generate_times
		self._remaining_chat_failures = fail_chat_times

	def _generate_once(
		self,
		prompt: str,
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs,
	) -> str:
		if self._remaining_generate_failures > 0:
			self._remaining_generate_failures -= 1
			raise _RetryableError("transient generate failure")
		return f"ok:{prompt}:{temperature}:{max_tokens}:{kwargs.get('provider') or ''}"

	def _chat_once(
		self,
		messages,
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs,
	) -> str:
		if self._remaining_chat_failures > 0:
			self._remaining_chat_failures -= 1
			raise _RetryableError("transient chat failure")
		return f"chat:{messages[-1].content}:{temperature}:{max_tokens}"


@pytest.mark.unit
def test_generate_retries_and_succeeds() -> None:
	policy = RetryPolicy(
		max_attempts=3,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	llm = FakeLLM(retry_policy=policy, fail_generate_times=2)

	result = llm.generate("hello", temperature=0.2, max_tokens=128, provider="openai")

	assert result == "ok:hello:0.2:128:openai"


@pytest.mark.unit
def test_chat_retries_and_normalizes_messages() -> None:
	policy = RetryPolicy(
		max_attempts=2,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	llm = FakeLLM(retry_policy=policy, fail_chat_times=1)

	result = llm.chat(
		[
			{"role": "system", "content": "你是审查助手"},
			ChatMessage(role="user", content="给出结论"),
		],
		temperature=0.1,
		max_tokens=64,
	)

	assert result == "chat:给出结论:0.1:64"


@pytest.mark.unit
def test_generate_raises_after_retry_exhausted() -> None:
	policy = RetryPolicy(
		max_attempts=2,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	llm = FakeLLM(retry_policy=policy, fail_generate_times=3)

	with pytest.raises(_RetryableError):
		llm.generate("will-fail")


@pytest.mark.unit
def test_chat_validates_empty_messages() -> None:
	llm = FakeLLM()

	with pytest.raises(ValueError, match="messages must not be empty"):
		llm.chat([])


@pytest.mark.unit
def test_retry_call_does_not_retry_non_retryable_errors() -> None:
	attempt = {"count": 0}

	def _op() -> str:
		attempt["count"] += 1
		raise ValueError("bad input")

	policy = RetryPolicy(max_attempts=3, base_delay_seconds=0, retry_exceptions=(_RetryableError,))

	with pytest.raises(ValueError):
		retry_call(_op, policy=policy)

	assert attempt["count"] == 1
