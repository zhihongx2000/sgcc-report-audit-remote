"""Unified LLM abstraction used by provider adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from utils.retry import RetryPolicy, retry_call


@dataclass(slots=True, frozen=True)
class ChatMessage:
	"""Normalized chat message structure shared by all providers."""

	role: str
	content: str


class BaseLLM(ABC):
	"""Base contract for all LLM providers.

	Provider implementations only need to implement `_generate_once` and
	`_chat_once`. Retry behavior is centralized at this layer.
	"""

	def __init__(self, *, retry_policy: RetryPolicy | None = None) -> None:
		self._retry_policy = retry_policy or RetryPolicy()

	@property
	def retry_policy(self) -> RetryPolicy:
		return self._retry_policy

	def generate(
		self,
		prompt: str,
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		"""Generate text from a single prompt with retry."""

		if not prompt:
			raise ValueError("prompt must not be empty")

		return retry_call(
			lambda: self._generate_once(
				prompt,
				temperature=temperature,
				max_tokens=max_tokens,
				**kwargs,
			),
			policy=self._retry_policy,
		)

	def chat(
		self,
		messages: Sequence[ChatMessage | Mapping[str, str]],
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		"""Generate text from multi-turn chat messages with retry."""

		normalized_messages = self._normalize_messages(messages)
		if not normalized_messages:
			raise ValueError("messages must not be empty")

		return retry_call(
			lambda: self._chat_once(
				normalized_messages,
				temperature=temperature,
				max_tokens=max_tokens,
				**kwargs,
			),
			policy=self._retry_policy,
		)

	@abstractmethod
	def _generate_once(
		self,
		prompt: str,
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		"""Provider-specific single-shot text generation."""

	@abstractmethod
	def _chat_once(
		self,
		messages: Sequence[ChatMessage],
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		"""Provider-specific chat completion."""

	@staticmethod
	def _normalize_messages(
		messages: Sequence[ChatMessage | Mapping[str, str]],
	) -> list[ChatMessage]:
		normalized: list[ChatMessage] = []
		for message in messages:
			if isinstance(message, ChatMessage):
				normalized.append(message)
				continue

			role = message.get("role")
			content = message.get("content")
			if not role or not content:
				raise ValueError("each message requires non-empty role and content")
			normalized.append(ChatMessage(role=role, content=content))

		return normalized
