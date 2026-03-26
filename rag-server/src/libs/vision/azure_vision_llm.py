"""Azure OpenAI Vision provider adapter (GPT-4o / GPT-4-Vision)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import openai

from libs.vision.base_vision_llm import BaseVisionLLM
from utils.retry import RetryPolicy

_DEFAULT_PROMPT = (
	"Please describe the content of this image in detail. "
	"If it contains charts, tables, or diagrams, extract the key data and "
	"structural information. Respond in the same language as any text visible "
	"in the image."
)


class AzureVisionLLM(BaseVisionLLM):
	"""Vision LLM adapter for Azure OpenAI (GPT-4o / GPT-4-Vision).

	Supports both local file paths (sent as base64 data URIs) and remote
	URLs (sent directly as ``image_url`` references).
	"""

	def __init__(
		self,
		*,
		endpoint: str,
		api_key: str,
		api_version: str,
		deployment_name: str,
		max_tokens: int = 1024,
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
		self._max_tokens = max_tokens

	def _caption_image_once(
		self,
		image_path: Path,
		*,
		prompt: str | None = None,
		**kwargs: Any,
	) -> str:
		resolved_prompt = prompt or _DEFAULT_PROMPT
		path_str = str(image_path)
		is_url = path_str.startswith(("http://", "https://"))

		if is_url:
			image_content: dict[str, Any] = {
				"type": "image_url",
				"image_url": {"url": path_str},
			}
		else:
			data_uri = self._encode_image_to_base64(image_path)
			image_content = {
				"type": "image_url",
				"image_url": {"url": data_uri},
			}

		messages: list[dict[str, Any]] = [
			{
				"role": "user",
				"content": [
					{"type": "text", "text": resolved_prompt},
					image_content,
				],
			}
		]

		create_kwargs: dict[str, Any] = {
			"model": self._deployment_name,
			"messages": messages,
			"max_tokens": self._max_tokens,
		}
		resp = self._client.chat.completions.create(**create_kwargs)
		return resp.choices[0].message.content or ""
