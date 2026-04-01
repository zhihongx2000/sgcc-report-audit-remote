"""Unit tests for BaseVisionLLM contract and retry behavior."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from libs.vision.base_vision_llm import BaseVisionLLM
from utils.retry import RetryPolicy


class _RetryableError(RuntimeError):
	pass


class FakeVisionLLM(BaseVisionLLM):
	"""Fake implementation for testing base contract behavior."""

	def __init__(
		self,
		*,
		retry_policy: RetryPolicy | None = None,
		fail_times: int = 0,
	) -> None:
		super().__init__(retry_policy=retry_policy)
		self._remaining_failures = fail_times
		self.call_count = 0

	def _caption_image_once(
		self,
		image_path: Path,
		*,
		prompt: str | None = None,
		**kwargs: Any,
	) -> str:
		self.call_count += 1
		if self._remaining_failures > 0:
			self._remaining_failures -= 1
			raise _RetryableError("transient vision failure")
		return f"caption:{image_path.name}:{prompt}:{kwargs.get('detail')}"


@pytest.mark.unit
def test_caption_image_retries_and_succeeds(tmp_path: Path) -> None:
	"""Test that caption_image retries on failure and eventually succeeds."""
	policy = RetryPolicy(
		max_attempts=3,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	vision = FakeVisionLLM(retry_policy=policy, fail_times=2)

	# Create a dummy image file
	test_image = tmp_path / "test.png"
	test_image.write_text("fake image data")

	result = vision.caption_image(test_image, prompt="describe this", detail="high")

	assert result == "caption:test.png:describe this:high"
	assert vision.call_count == 3


@pytest.mark.unit
def test_caption_image_raises_after_retry_exhausted(tmp_path: Path) -> None:
	"""Test that caption_image raises when all retries are exhausted."""
	policy = RetryPolicy(
		max_attempts=2,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	vision = FakeVisionLLM(retry_policy=policy, fail_times=3)

	test_image = tmp_path / "test.png"
	test_image.write_text("fake image data")

	with pytest.raises(_RetryableError):
		vision.caption_image(test_image)


@pytest.mark.unit
def test_caption_image_validates_empty_path() -> None:
	"""Test that empty image_path raises ValueError."""
	vision = FakeVisionLLM()

	with pytest.raises(ValueError, match="image_path must not be empty"):
		vision.caption_image("")


@pytest.mark.unit
def test_caption_image_validates_nonexistent_file() -> None:
	"""Test that non-existent file raises FileNotFoundError."""
	vision = FakeVisionLLM()

	with pytest.raises(FileNotFoundError):
		vision.caption_image("/path/that/does/not/exist.png")


@pytest.mark.unit
def test_caption_image_accepts_url() -> None:
	"""Test that URL image paths work without file existence check."""
	policy = RetryPolicy(
		max_attempts=1,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	vision = FakeVisionLLM(retry_policy=policy)

	result = vision.caption_image("https://example.com/image.png", prompt="test")

	assert "caption:image.png:test" in result


@pytest.mark.unit
def test_caption_image_default_prompt(tmp_path: Path) -> None:
	"""Test that None prompt is passed through to implementation."""
	policy = RetryPolicy(
		max_attempts=1,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	vision = FakeVisionLLM(retry_policy=policy)

	test_image = tmp_path / "chart.jpg"
	test_image.write_text("fake image data")

	result = vision.caption_image(test_image)

	assert "caption:chart.jpg:None" in result


@pytest.mark.unit
def test_caption_image_accepts_path_object(tmp_path: Path) -> None:
	"""Test that Path objects are accepted."""
	policy = RetryPolicy(
		max_attempts=1,
		base_delay_seconds=0,
		retry_exceptions=(_RetryableError,),
	)
	vision = FakeVisionLLM(retry_policy=policy)

	test_image = tmp_path / "document.png"
	test_image.write_text("fake image data")

	result = vision.caption_image(test_image, prompt="analyze")

	assert "caption:document.png:analyze" in result


@pytest.mark.unit
def test_encode_image_to_base64(tmp_path: Path) -> None:
	"""Test base64 encoding utility."""
	test_image = tmp_path / "test.png"
	test_image.write_bytes(b"fake image bytes")

	encoded = BaseVisionLLM._encode_image_to_base64(test_image)

	assert encoded.startswith("data:image/png;base64,")
	# Decode and verify
	import base64
	decoded = base64.b64decode(encoded.split(",")[1])
	assert decoded == b"fake image bytes"


@pytest.mark.unit
def test_encode_image_default_mimetype(tmp_path: Path) -> None:
	"""Test that unknown extensions get default jpeg mimetype."""
	test_image = tmp_path / "test.unknown"
	test_image.write_bytes(b"fake data")

	encoded = BaseVisionLLM._encode_image_to_base64(test_image)

	assert encoded.startswith("data:image/jpeg;base64,")
