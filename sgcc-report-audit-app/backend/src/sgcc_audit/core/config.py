"""Backend configuration loader with file/env precedence.

Current scope intentionally matches A4 baseline fields. Full DEV_SPEC 5.6
coverage and stronger config model validation are scheduled in D10.
"""

from __future__ import annotations

from functools import lru_cache
import os
from pathlib import Path
from typing import Any, Callable

import yaml
from pydantic import BaseModel, Field


class LLMSettings(BaseModel):
	"""LLM settings used by backend orchestration."""

	provider: str = Field(min_length=1)
	model: str = Field(min_length=1)
	api_key: str = Field(min_length=1)
	timeout_seconds: int = Field(default=30, ge=1)


class MCPClientSettings(BaseModel):
	"""Settings for MCP subprocess invocation."""

	command: str = Field(min_length=1)
	timeout_seconds: int = Field(default=30, ge=1)


class Settings(BaseModel):
	"""Top-level backend settings model."""

	service_name: str = Field(default="sgcc-audit-backend", min_length=1)
	environment: str = Field(default="development", min_length=1)
	mcp_client: MCPClientSettings
	llm: LLMSettings


_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[4] / "config" / "settings.yaml"

_ENV_OVERRIDES: tuple[tuple[str, tuple[str, ...], Callable[[str], Any]], ...] = (
	("SGCC_BACKEND_SERVICE_NAME", ("service_name",), str),
	("SGCC_BACKEND_ENVIRONMENT", ("environment",), str),
	("SGCC_BACKEND_MCP_COMMAND", ("mcp_client", "command"), str),
	("SGCC_BACKEND_MCP_TIMEOUT_SECONDS", ("mcp_client", "timeout_seconds"), int),
	("SGCC_BACKEND_LLM_PROVIDER", ("llm", "provider"), str),
	("SGCC_BACKEND_LLM_MODEL", ("llm", "model"), str),
	("SGCC_BACKEND_LLM_API_KEY", ("llm", "api_key"), str),
	("SGCC_BACKEND_LLM_TIMEOUT_SECONDS", ("llm", "timeout_seconds"), int),
)


def _read_yaml(config_path: Path) -> dict[str, Any]:
	if not config_path.exists():
		raise FileNotFoundError(f"Settings file not found: {config_path}")

	with config_path.open("r", encoding="utf-8") as f:
		loaded = yaml.safe_load(f)

	if loaded is None:
		return {}
	if not isinstance(loaded, dict):
		raise ValueError(f"Settings file must contain a YAML mapping: {config_path}")

	return dict(loaded)


def _set_nested_value(payload: dict[str, Any], path: tuple[str, ...], value: Any) -> None:
	current = payload
	for key in path[:-1]:
		next_item = current.get(key)
		if not isinstance(next_item, dict):
			next_item = {}
			current[key] = next_item
		current = next_item
	current[path[-1]] = value


def _apply_env_overrides(payload: dict[str, Any]) -> dict[str, Any]:
	merged = dict(payload)
	for env_name, path, parser in _ENV_OVERRIDES:
		raw_value = os.getenv(env_name)
		if raw_value is None:
			continue
		parsed_value = parser(raw_value)
		_set_nested_value(merged, path, parsed_value)
	return merged


def load_settings(config_path: str | Path | None = None) -> Settings:
	"""Load backend settings with precedence: env > file > defaults."""

	resolved_path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
	payload = _read_yaml(resolved_path)
	merged = _apply_env_overrides(payload)
	return Settings.model_validate(merged)


@lru_cache(maxsize=1)
def _load_cached_default() -> Settings:
	return load_settings()


def get_config(*, force_reload: bool = False) -> Settings:
	"""Get cached backend config loaded from default config path."""

	if force_reload:
		_load_cached_default.cache_clear()
	return _load_cached_default()
