"""Configuration loading for rag-server.

Priority order is: environment variables > YAML file values > model defaults.

Current scope intentionally matches A4 baseline fields. Full DEV_SPEC 5.6
coverage and stronger config model validation are scheduled in D10.

D6 additions: PostgresSettings and VectorStoreSettings for DB connectivity.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import yaml
from pydantic import BaseModel, ConfigDict, Field


class LLMSettings(BaseModel):
	"""LLM provider settings used by retrieval/generation flows."""

	provider: str = Field(min_length=1)
	model: str = Field(min_length=1)
	api_key: str = Field(min_length=1)
	timeout_seconds: int = Field(default=30, ge=1)


class RetrievalSettings(BaseModel):
	"""Retrieval behavior settings."""

	top_k: int = Field(default=5, ge=1)


class PostgresSettings(BaseModel):
	"""PostgreSQL connection settings."""

	host: str = Field(default="localhost")
	port: int = Field(default=5432, ge=1)
	database: str = Field(default="postgres")
	user: str = Field(default="postgres")
	password: str = Field(default="")
	schema_name: str = Field(default="public", alias="schema")
	sslmode: str = Field(default="disable")
	pool_size: int = Field(default=5, ge=1)
	pool_timeout_sec: int = Field(default=30, ge=1)
	statement_timeout_ms: int = Field(default=30000, ge=0)

	model_config = ConfigDict(populate_by_name=True)


class VectorStoreSettings(BaseModel):
	"""Vector store configuration."""

	backend: str = Field(default="pgvector")
	table: str = Field(default="rag_chunks")
	embedding_dim: int = Field(default=1536, ge=1)
	distance_metric: str = Field(default="cosine")
	enable_sparse_fields: bool = Field(default=True)
	metadata_jsonb: bool = Field(default=True)


class RerankSettings(BaseModel):
	"""Reranker configuration.

	D7 additions: backend selector, model name, and operational limits.
	Full env-override wiring is scheduled in D10.
	"""

	backend: str = Field(default="cross_encoder")  # none | cross_encoder | llm
	model: str = Field(default="BAAI/bge-reranker-v2-m3")
	max_candidates: int = Field(default=30, ge=1)
	timeout_sec: float = Field(default=10.0, gt=0)
	fallback_to_none: bool = Field(default=True)


class Settings(BaseModel):
	"""Top-level rag-server settings model."""

	app_name: str = Field(default="rag-mcp-server", min_length=1)
	environment: str = Field(default="development", min_length=1)
	llm: LLMSettings
	retrieval: RetrievalSettings = Field(default_factory=RetrievalSettings)
	postgres: PostgresSettings = Field(default_factory=PostgresSettings)
	vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)
	rerank: RerankSettings = Field(default_factory=RerankSettings)


_DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "settings.yaml"

_ENV_OVERRIDES: tuple[tuple[str, tuple[str, ...], Callable[[str], Any]], ...] = (
	("RAG_APP_NAME", ("app_name",), str),
	("RAG_ENVIRONMENT", ("environment",), str),
	("RAG_LLM_PROVIDER", ("llm", "provider"), str),
	("RAG_LLM_MODEL", ("llm", "model"), str),
	("RAG_LLM_API_KEY", ("llm", "api_key"), str),
	("RAG_LLM_TIMEOUT_SECONDS", ("llm", "timeout_seconds"), int),
	("RAG_RETRIEVAL_TOP_K", ("retrieval", "top_k"), int),
	# D6: PostgreSQL env overrides
	("PG_HOST", ("postgres", "host"), str),
	("PG_PORT", ("postgres", "port"), int),
	("PG_DATABASE", ("postgres", "database"), str),
	("PG_USER", ("postgres", "user"), str),
	("PG_PASSWORD", ("postgres", "password"), str),
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
	"""Load settings with precedence: env > file > defaults."""

	resolved_path = Path(config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
	payload = _read_yaml(resolved_path)
	merged = _apply_env_overrides(payload)
	return Settings.model_validate(merged)
