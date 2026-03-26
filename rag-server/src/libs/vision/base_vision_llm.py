"""Unified Vision LLM abstraction used by provider adapters."""

from __future__ import annotations

import base64
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from utils.retry import RetryPolicy, retry_call

_MIME_MAP: dict[str, str] = {
	".png": "image/png",
	".jpg": "image/jpeg",
	".jpeg": "image/jpeg",
	".gif": "image/gif",
	".webp": "image/webp",
	".bmp": "image/bmp",
}


class BaseVisionLLM(ABC):
	"""Base contract for all Vision LLM providers.

	Provider implementations only need to implement ``_caption_image_once``.
	Retry behavior and input validation are centralized at this layer.
	"""

	def __init__(self, *, retry_policy: RetryPolicy | None = None) -> None:
		self._retry_policy = retry_policy or RetryPolicy()

	@property
	def retry_policy(self) -> RetryPolicy:
		return self._retry_policy

	def caption_image(
		self,
		image_path: Path | str,
		*,
		prompt: str | None = None,
		**kwargs: Any,
	) -> str:
		"""Generate a text caption for the given image with retry.

		Accepts a local file path or a URL. Local paths are validated for
		existence; URL paths skip file-system checks.

		Args:
			image_path: Absolute local file path or ``http(s)://`` URL.
			prompt: Optional custom captioning prompt. If ``None``, the
				provider uses its own default prompt.
			**kwargs: Extra provider-specific keyword arguments forwarded
				to ``_caption_image_once``.

		Returns:
			A non-empty description string.

		Raises:
			ValueError: If ``image_path`` is empty.
			FileNotFoundError: If a local path does not exist.
		"""
		if not image_path:
			raise ValueError("image_path must not be empty")

		path_str = str(image_path)
		is_url = path_str.startswith(("http://", "https://"))
		path = Path(image_path)

		if not is_url and not path.exists():
			raise FileNotFoundError(f"Image file not found: {image_path}")

		return retry_call(
			lambda: self._caption_image_once(path, prompt=prompt, **kwargs),
			policy=self._retry_policy,
		)

	@abstractmethod
	def _caption_image_once(
		self,
		image_path: Path,
		*,
		prompt: str | None = None,
		**kwargs: Any,
	) -> str:
		"""Provider-specific single-shot image captioning (no retry)."""

	@staticmethod
	def _encode_image_to_base64(image_path: Path) -> str:
		"""Return a data-URI string ``data:<mime>;base64,<encoded>``.

		Unknown extensions default to ``image/jpeg``.
		"""
		suffix = image_path.suffix.lower()
		mime_type = _MIME_MAP.get(suffix, "image/jpeg")
		image_bytes = image_path.read_bytes()
		encoded = base64.b64encode(image_bytes).decode("utf-8")
		return f"data:{mime_type};base64,{encoded}"
