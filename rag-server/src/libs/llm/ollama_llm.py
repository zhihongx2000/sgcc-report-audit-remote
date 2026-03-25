"""Ollama local provider adapter using the native ollama SDK."""

from __future__ import annotations

from typing import Any, Sequence

import ollama as _ollama

from libs.llm.base_llm import BaseLLM, ChatMessage
from utils.retry import RetryPolicy


class OllamaLLM(BaseLLM):
	"""LLM adapter for locally hosted Ollama server."""

	def __init__(
		self,
		*,
		model: str,
		base_url: str = "http://localhost:11434",
		temperature: float | None = None,
		max_tokens: int | None = None,
		timeout_seconds: float = 60.0,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._client = _ollama.Client(host=base_url, timeout=timeout_seconds)
		self._model = model
		self._temperature = temperature
		self._max_tokens = max_tokens

	def _generate_once(
		self,
		prompt: str,
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		return self._chat_once(
			[ChatMessage(role="user", content=prompt)],
			temperature=temperature,
			max_tokens=max_tokens,
			**kwargs,
		)

	def _chat_once(
		self,
		messages: Sequence[ChatMessage],
		*,
		temperature: float | None = None,
		max_tokens: int | None = None,
		**kwargs: Any,
	) -> str:
		api_msgs = [{"role": m.role, "content": m.content} for m in messages]
		options: dict[str, Any] = {}
		resolved_temp = temperature if temperature is not None else self._temperature
		resolved_max = max_tokens if max_tokens is not None else self._max_tokens
		if resolved_temp is not None:
			options["temperature"] = resolved_temp
		if resolved_max is not None:
			options["num_predict"] = resolved_max
		resp = self._client.chat(model=self._model, messages=api_msgs, options=options)
		return resp.message.content
