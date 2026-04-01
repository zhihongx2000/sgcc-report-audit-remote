"""Factory for creating LLM instances from configuration."""

from __future__ import annotations

from core.settings import LLMSettings
from libs.llm.azure_openai_llm import AzureOpenAILLM
from libs.llm.base_llm import BaseLLM
from libs.llm.deepseek_llm import DeepSeekLLM
from libs.llm.ollama_llm import OllamaLLM
from libs.llm.openai_llm import OpenAILLM
from libs.llm.qwen_llm import QwenLLM
from libs.llm.vllm_llm import VLLMLLM


def create_llm(settings: LLMSettings, **kwargs) -> BaseLLM:  # noqa: ANN003
    """Instantiate an LLM from *settings*.

    Args:
        settings: LLM settings section from the application config.
        **kwargs: Provider-specific overrides.
            - ``azure``: ``endpoint``, ``api_version``, ``deployment_name``.
            - ``vllm``: ``base_url``.
            - ``ollama``: ``base_url`` (optional, defaults to localhost).

    Returns:
        A concrete :class:`BaseLLM` instance.

    Raises:
        ValueError: If *settings.provider* is not a registered provider.
        KeyError: If a required provider-specific kwarg is missing.
    """
    provider = settings.provider.lower().strip()
    timeout = float(settings.timeout_seconds)

    if provider == "openai":
        return OpenAILLM(
            api_key=settings.api_key,
            model=settings.model,
            timeout_seconds=timeout,
        )
    if provider == "qwen":
        return QwenLLM(
            api_key=settings.api_key,
            model=settings.model,
            timeout_seconds=timeout,
        )
    if provider == "azure":
        return AzureOpenAILLM(
            endpoint=kwargs["endpoint"],
            api_key=settings.api_key,
            api_version=kwargs["api_version"],
            deployment_name=kwargs.get("deployment_name", settings.model),
            timeout_seconds=timeout,
        )
    if provider == "deepseek":
        return DeepSeekLLM(
            api_key=settings.api_key,
            model=settings.model,
            timeout_seconds=timeout,
        )
    if provider == "vllm":
        return VLLMLLM(
            base_url=kwargs["base_url"],
            model=settings.model,
            timeout_seconds=timeout,
        )
    if provider == "ollama":
        return OllamaLLM(
            model=settings.model,
            base_url=kwargs.get("base_url", "http://localhost:11434"),
            timeout_seconds=timeout,
        )
    raise ValueError(
        f"Unknown LLM provider '{settings.provider}'. "
        "Available providers: azure, deepseek, ollama, openai, qwen, vllm"
    )
