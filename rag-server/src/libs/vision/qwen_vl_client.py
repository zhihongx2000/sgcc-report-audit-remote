"""Qwen-VL provider adapter — via DashScope OpenAI-compatible endpoint."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import openai

from libs.vision.base_vision_llm import BaseVisionLLM
from utils.retry import RetryPolicy

_DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

_DEFAULT_PROMPT = (
	"请详细描述这张图片的内容。"
	"如果图片包含图表、表格或流程图，请提取关键数据和结构信息。"
	"如果图片包含文字，请准确转录并说明其含义。"
)


class QwenVLClient(BaseVisionLLM):
	"""Vision LLM adapter for Qwen-VL via DashScope OpenAI-compatible endpoint.

	Supports both local file paths (sent as base64 data URIs) and remote
	URLs (sent directly as image references).
	"""

	def __init__(
		self,
		*,
		api_key: str,
		model: str,
		base_url: str = _DASHSCOPE_BASE_URL,
		max_tokens: int = 1024,
		timeout_seconds: float = 60.0,
		retry_policy: RetryPolicy | None = None,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._client = openai.OpenAI(
			api_key=api_key,
			base_url=base_url,
			timeout=timeout_seconds,
		)
		self._model = model
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
			image_ref: dict[str, Any] = {
				"type": "image_url",
				"image_url": {"url": path_str},
			}
		else:
			data_uri = self._encode_image_to_base64(image_path)
			image_ref = {
				"type": "image_url",
				"image_url": {"url": data_uri},
			}

		messages: list[dict[str, Any]] = [
			{
				"role": "user",
				"content": [
					image_ref,
					{"type": "text", "text": resolved_prompt},
				],
			}
		]

		create_kwargs: dict[str, Any] = {
			"model": self._model,
			"messages": messages,
			"max_tokens": self._max_tokens,
		}
		resp = self._client.chat.completions.create(**create_kwargs)
		return resp.choices[0].message.content or ""
