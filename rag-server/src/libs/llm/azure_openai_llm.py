"""Azure OpenAI provider adapter."""

from __future__ import annotations

from typing import Any, Sequence

import openai

from libs.llm.base_llm import BaseLLM, ChatMessage
from utils.retry import RetryPolicy


class AzureOpenAILLM(BaseLLM):
	"""LLM adapter for Azure OpenAI.

	Uses ``deployment_name`` as the model identifier; the endpoint and
	api_version are required Azure-specific parameters.
	"""

	def __init__(
		self,
		*,
		endpoint: str,
		api_key: str,
		api_version: str,
		deployment_name: str,
		temperature: float | None = None,
		max_tokens: int | None = None,
		timeout_seconds: float = 60.0,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._client = openai.AzureOpenAI(
			azure_endpoint=endpoint,
			api_key=api_key,
			api_version=api_version,
			timeout=timeout_seconds,
		)
		self._deployment_name = deployment_name
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
		create_kwargs: dict[str, Any] = {
			"model": self._deployment_name,
			"messages": api_msgs,
		}
		resolved_temp = temperature if temperature is not None else self._temperature
		resolved_max = max_tokens if max_tokens is not None else self._max_tokens
		if resolved_temp is not None:
			create_kwargs["temperature"] = resolved_temp
		if resolved_max is not None:
			create_kwargs["max_tokens"] = resolved_max
		resp = self._client.chat.completions.create(**create_kwargs)
		return resp.choices[0].message.content
