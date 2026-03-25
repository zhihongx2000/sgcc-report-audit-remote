"""Unit tests for LLM provider adapters using fake transports (mocks).

Each provider is tested for:
- generate() wraps prompt as a user chat message
- chat() passes normalized messages correctly
- call-time temperature/max_tokens override instance defaults
- instance defaults are used when call-time values are None
- response content is extracted and returned as a plain string
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from libs.llm.azure_openai_llm import AzureOpenAILLM
from libs.llm.base_llm import ChatMessage
from libs.llm.deepseek_llm import DeepSeekLLM
from libs.llm.ollama_llm import OllamaLLM
from libs.llm.openai_llm import OpenAILLM
from libs.llm.qwen_llm import QwenLLM
from libs.llm.vllm_llm import VLLMLLM
from utils.retry import RetryPolicy


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_NO_RETRY = RetryPolicy(max_attempts=1, base_delay_seconds=0)


def _openai_response(content: str) -> MagicMock:
	"""Build a minimal fake openai ChatCompletion response."""
	choice = MagicMock()
	choice.message.content = content
	resp = MagicMock()
	resp.choices = [choice]
	return resp


def _ollama_response(content: str) -> MagicMock:
	"""Build a minimal fake ollama ChatResponse."""
	resp = MagicMock()
	resp.message.content = content
	return resp


# ---------------------------------------------------------------------------
# OpenAILLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.openai_llm.openai.OpenAI")
def test_openai_generate_wraps_prompt_as_user_message(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("pong")

	llm = OpenAILLM(api_key="k", model="gpt-4o", retry_policy=_NO_RETRY)
	result = llm.generate("ping")

	assert result == "pong"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["model"] == "gpt-4o"
	assert call_kwargs["messages"] == [{"role": "user", "content": "ping"}]


@pytest.mark.unit
@patch("libs.llm.openai_llm.openai.OpenAI")
def test_openai_chat_passes_messages(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("result")

	llm = OpenAILLM(
		api_key="k", model="gpt-4o", temperature=0.5, max_tokens=100, retry_policy=_NO_RETRY
	)
	result = llm.chat([ChatMessage(role="user", content="hello")])

	assert result == "result"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["temperature"] == 0.5
	assert call_kwargs["max_tokens"] == 100


@pytest.mark.unit
@patch("libs.llm.openai_llm.openai.OpenAI")
def test_openai_call_time_params_override_defaults(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("overridden")

	llm = OpenAILLM(
		api_key="k", model="gpt-4o", temperature=0.1, max_tokens=50, retry_policy=_NO_RETRY
	)
	llm.generate("x", temperature=0.9, max_tokens=200)

	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["temperature"] == 0.9
	assert call_kwargs["max_tokens"] == 200


@pytest.mark.unit
@patch("libs.llm.openai_llm.openai.OpenAI")
def test_openai_omits_none_temperature_and_max_tokens(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("no-params")

	llm = OpenAILLM(api_key="k", model="gpt-4o", retry_policy=_NO_RETRY)
	llm.generate("x")

	call_kwargs = mock_create.call_args.kwargs
	assert "temperature" not in call_kwargs
	assert "max_tokens" not in call_kwargs


# ---------------------------------------------------------------------------
# AzureOpenAILLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.azure_openai_llm.openai.AzureOpenAI")
def test_azure_generate_uses_deployment_name(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("azure-resp")

	llm = AzureOpenAILLM(
		endpoint="https://my-resource.openai.azure.com",
		api_key="k",
		api_version="2024-10-21",
		deployment_name="gpt-4o-deploy",
		retry_policy=_NO_RETRY,
	)
	result = llm.generate("hello")

	assert result == "azure-resp"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["model"] == "gpt-4o-deploy"
	assert call_kwargs["messages"] == [{"role": "user", "content": "hello"}]


@pytest.mark.unit
@patch("libs.llm.azure_openai_llm.openai.AzureOpenAI")
def test_azure_initialised_with_correct_endpoint(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ok")

	AzureOpenAILLM(
		endpoint="https://endpoint.azure.com",
		api_key="key123",
		api_version="2024-10-21",
		deployment_name="d1",
		retry_policy=_NO_RETRY,
	)

	mock_cls.assert_called_once()
	init_kwargs = mock_cls.call_args.kwargs
	assert init_kwargs["azure_endpoint"] == "https://endpoint.azure.com"
	assert init_kwargs["api_version"] == "2024-10-21"


# ---------------------------------------------------------------------------
# DeepSeekLLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.deepseek_llm.openai.OpenAI")
def test_deepseek_uses_deepseek_base_url(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ds")

	DeepSeekLLM(api_key="k", model="deepseek-chat", retry_policy=_NO_RETRY)

	init_kwargs = mock_cls.call_args.kwargs
	assert "deepseek" in init_kwargs["base_url"]


@pytest.mark.unit
@patch("libs.llm.deepseek_llm.openai.OpenAI")
def test_deepseek_generate(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("deepseek-answer")

	llm = DeepSeekLLM(api_key="k", model="deepseek-chat", retry_policy=_NO_RETRY)
	result = llm.generate("question")

	assert result == "deepseek-answer"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["model"] == "deepseek-chat"
	assert call_kwargs["messages"] == [{"role": "user", "content": "question"}]


# ---------------------------------------------------------------------------
# QwenLLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.qwen_llm.openai.OpenAI")
def test_qwen_uses_dashscope_base_url(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ok")

	QwenLLM(api_key="k", model="qwen-plus", retry_policy=_NO_RETRY)

	init_kwargs = mock_cls.call_args.kwargs
	assert "dashscope" in init_kwargs["base_url"]


@pytest.mark.unit
@patch("libs.llm.qwen_llm.openai.OpenAI")
def test_qwen_custom_base_url(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ok")

	QwenLLM(
		api_key="k",
		model="qwen-plus",
		base_url="https://custom.api/v1",
		retry_policy=_NO_RETRY,
	)

	init_kwargs = mock_cls.call_args.kwargs
	assert init_kwargs["base_url"] == "https://custom.api/v1"


@pytest.mark.unit
@patch("libs.llm.qwen_llm.openai.OpenAI")
def test_qwen_chat(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("qwen-result")

	llm = QwenLLM(
		api_key="k", model="qwen-plus", temperature=0.2, max_tokens=512, retry_policy=_NO_RETRY
	)
	result = llm.chat(
		[
			{"role": "system", "content": "You are an assistant"},
			{"role": "user", "content": "Hi"},
		]
	)

	assert result == "qwen-result"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["temperature"] == 0.2
	assert call_kwargs["max_tokens"] == 512
	assert len(call_kwargs["messages"]) == 2


# ---------------------------------------------------------------------------
# VLLMLLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.vllm_llm.openai.OpenAI")
def test_vllm_uses_provided_base_url(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ok")

	VLLMLLM(base_url="http://localhost:8000/v1", model="llama3", retry_policy=_NO_RETRY)

	init_kwargs = mock_cls.call_args.kwargs
	assert init_kwargs["base_url"] == "http://localhost:8000/v1"


@pytest.mark.unit
@patch("libs.llm.vllm_llm.openai.OpenAI")
def test_vllm_generate(mock_cls: MagicMock) -> None:
	mock_create = mock_cls.return_value.chat.completions.create
	mock_create.return_value = _openai_response("vllm-answer")

	llm = VLLMLLM(
		base_url="http://localhost:8000/v1", model="llama3", retry_policy=_NO_RETRY
	)
	result = llm.generate("prompt")

	assert result == "vllm-answer"
	call_kwargs = mock_create.call_args.kwargs
	assert call_kwargs["model"] == "llama3"
	assert call_kwargs["messages"] == [{"role": "user", "content": "prompt"}]


@pytest.mark.unit
@patch("libs.llm.vllm_llm.openai.OpenAI")
def test_vllm_uses_vllm_api_key_by_default(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.completions.create.return_value = _openai_response("ok")

	VLLMLLM(base_url="http://localhost:8000/v1", model="llama3", retry_policy=_NO_RETRY)

	init_kwargs = mock_cls.call_args.kwargs
	assert init_kwargs["api_key"] == "vllm"


# ---------------------------------------------------------------------------
# OllamaLLM
# ---------------------------------------------------------------------------


@pytest.mark.unit
@patch("libs.llm.ollama_llm._ollama.Client")
def test_ollama_generate_wraps_prompt(mock_cls: MagicMock) -> None:
	mock_chat = mock_cls.return_value.chat
	mock_chat.return_value = _ollama_response("ollama-answer")

	llm = OllamaLLM(model="llama3", retry_policy=_NO_RETRY)
	result = llm.generate("prompt")

	assert result == "ollama-answer"
	call_kwargs = mock_chat.call_args.kwargs
	assert call_kwargs["model"] == "llama3"
	assert call_kwargs["messages"] == [{"role": "user", "content": "prompt"}]


@pytest.mark.unit
@patch("libs.llm.ollama_llm._ollama.Client")
def test_ollama_chat_passes_temperature_in_options(mock_cls: MagicMock) -> None:
	mock_chat = mock_cls.return_value.chat
	mock_chat.return_value = _ollama_response("ok")

	llm = OllamaLLM(model="llama3", temperature=0.7, retry_policy=_NO_RETRY)
	llm.chat([ChatMessage(role="user", content="hello")])

	call_kwargs = mock_chat.call_args.kwargs
	assert call_kwargs["options"]["temperature"] == 0.7


@pytest.mark.unit
@patch("libs.llm.ollama_llm._ollama.Client")
def test_ollama_max_tokens_maps_to_num_predict(mock_cls: MagicMock) -> None:
	mock_chat = mock_cls.return_value.chat
	mock_chat.return_value = _ollama_response("ok")

	llm = OllamaLLM(model="llama3", max_tokens=256, retry_policy=_NO_RETRY)
	llm.generate("x")

	call_kwargs = mock_chat.call_args.kwargs
	assert call_kwargs["options"]["num_predict"] == 256


@pytest.mark.unit
@patch("libs.llm.ollama_llm._ollama.Client")
def test_ollama_uses_custom_base_url(mock_cls: MagicMock) -> None:
	mock_cls.return_value.chat.return_value = _ollama_response("ok")

	OllamaLLM(model="llama3", base_url="http://remote:11434", retry_policy=_NO_RETRY)

	init_kwargs = mock_cls.call_args.kwargs
	assert init_kwargs["host"] == "http://remote:11434"


@pytest.mark.unit
@patch("libs.llm.ollama_llm._ollama.Client")
def test_ollama_call_time_temperature_overrides_default(mock_cls: MagicMock) -> None:
	mock_chat = mock_cls.return_value.chat
	mock_chat.return_value = _ollama_response("ok")

	llm = OllamaLLM(model="llama3", temperature=0.1, retry_policy=_NO_RETRY)
	llm.generate("x", temperature=0.99)

	call_kwargs = mock_chat.call_args.kwargs
	assert call_kwargs["options"]["temperature"] == 0.99
