"""Factory for creating Vision LLM instances from configuration."""

from __future__ import annotations

from libs.vision.azure_vision_llm import AzureVisionLLM
from libs.vision.base_vision_llm import BaseVisionLLM
from libs.vision.qwen_vl_client import QwenVLClient


def create_vision_llm(provider: str, **kwargs) -> BaseVisionLLM:  # noqa: ANN003
    """Instantiate a Vision LLM by *provider* name.

    Args:
        provider: Vision LLM provider identifier (``"azure"`` or ``"qwen"``).  
        **kwargs: Provider-specific keyword arguments forwarded to the
            constructor.  Required kwargs per provider:
            - ``azure``: ``endpoint``, ``api_key``, ``api_version``,
              ``deployment_name``.
            - ``qwen``: ``api_key``, ``model``.

    Returns:
        A concrete :class:`BaseVisionLLM` instance.

    Raises:
        ValueError: If *provider* is not a registered provider.
        KeyError: If a required provider-specific kwarg is missing.
    """
    _provider = provider.lower().strip()

    if _provider == "azure":
        return AzureVisionLLM(
            endpoint=kwargs["endpoint"],
            api_key=kwargs["api_key"],
            api_version=kwargs["api_version"],
            deployment_name=kwargs["deployment_name"],
            max_tokens=kwargs.get("max_tokens", 1024),
            timeout_seconds=float(kwargs.get("timeout_seconds", 60.0)),
        )
    if _provider == "qwen":
        return QwenVLClient(
            api_key=kwargs["api_key"],
            model=kwargs["model"],
            max_tokens=kwargs.get("max_tokens", 1024),
            timeout_seconds=float(kwargs.get("timeout_seconds", 60.0)),
        )
    raise ValueError(
        f"Unknown Vision LLM provider '{provider}'. "
        "Available providers: azure, qwen"
    )
