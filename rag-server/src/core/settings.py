"""Configuration loading for rag-server.

Priority order is: environment variables > YAML file values > model defaults.

D10: Full DEV_SPEC 5.6 coverage — all component config sections modelled,
validate_settings() enforces semantic rules at startup.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator


# ---------------------------------------------------------------------------
# Sub-section models
# ---------------------------------------------------------------------------


class AppSettings(BaseModel):
    """Top-level app identity and runtime env."""

    env: str = Field(default="local")  # local | test | prod
    log_level: str = Field(default="INFO")


class LLMSettings(BaseModel):
    """LLM provider settings used by retrieval/generation flows."""

    provider: str = Field(min_length=1)
    model: str = Field(min_length=1)
    api_key: str = Field(min_length=1)
    timeout_seconds: int = Field(default=30, ge=1)
    # Extended fields for full provider support (optional)
    temperature: float = Field(default=0.1, ge=0.0, le=2.0)
    max_tokens: int = Field(default=2000, ge=1)
    endpoint: str | None = Field(default=None)
    api_version: str | None = Field(default=None)
    deployment_name: str | None = Field(default=None)
    base_url: str | None = Field(default=None)


class MineruAPISettings(BaseModel):
    """Mineru API backend configuration."""

    base_url: str = Field(default="https://mineru.net/api/v4")
    api_token: str = Field(default="")
    timeout_sec: int = Field(default=120, ge=1)


class MineruLocalSettings(BaseModel):
    """Mineru local Docker backend configuration."""

    endpoint: str = Field(default="http://localhost:8888")
    timeout_sec: int = Field(default=120, ge=1)


class LoaderSettings(BaseModel):
    """Document loader backend configuration."""

    # markitdown | mineru_api | mineru_local
    backend: str = Field(default="markitdown")
    mineru_api: MineruAPISettings = Field(default_factory=MineruAPISettings)
    mineru_local: MineruLocalSettings = Field(
        default_factory=MineruLocalSettings)


class EmbeddingSettings(BaseModel):
    """Embedding provider configuration."""

    # openai | azure | ollama | bge | openai-compatible
    provider: str = Field(default="bge")
    model: str = Field(default="BAAI/bge-large-zh-v1.5")
    embedding_dim: int = Field(default=1024, ge=1)
    batch_size: int = Field(default=64, ge=1)
    timeout_sec: float = Field(default=30.0, gt=0)
    model_cache_dir: str = Field(default="./models")


class VisionLLMSettings(BaseModel):
    """Vision LLM provider configuration."""

    # azure | qwen-vl | openai-compatible
    provider: str = Field(default="qwen-vl")
    model: str = Field(default="qwen-vl-max")
    api_key: str = Field(default="")
    base_url: str = Field(default="")
    timeout_sec: float = Field(default=60.0, gt=0)


class SplitterSettings(BaseModel):
    """Document splitter configuration."""

    # recursive_character | parent_child
    backend: str = Field(default="recursive_character")
    chunk_size: int = Field(default=1000, ge=1)
    chunk_overlap: int = Field(default=150, ge=0)
    separators: list[str] = Field(default_factory=lambda: [
                                  "\n\n", "\n", "。", "；", "，", " "])
    enable_parent_child: bool = Field(default=True)
    parent_trigger_k: int = Field(default=3, ge=1)

    @field_validator("chunk_overlap")
    @classmethod
    def overlap_less_than_chunk_size(cls, v: int, info: Any) -> int:
        chunk_size = info.data.get("chunk_size", 1000)
        if v >= chunk_size:
            raise ValueError(
                f"chunk_overlap ({v}) must be less than chunk_size ({chunk_size})")
        return v


class RetrievalSettings(BaseModel):
    """Retrieval behavior settings."""

    # Legacy field kept for backward compatibility with A4 baseline tests
    top_k: int = Field(default=5, ge=1)
    # Extended retrieval settings (D10: 5.6 alignment)
    mode: str = Field(default="hybrid")  # dense | sparse | hybrid
    sparse_backend: str = Field(default="bm25")
    dense_top_k: int = Field(default=30, ge=1)
    sparse_top_k: int = Field(default=30, ge=1)
    fusion_algorithm: str = Field(default="rrf")  # rrf | weighted_sum
    fusion_k: int = Field(default=60, ge=1)
    final_top_k: int = Field(default=10, ge=1)
    score_threshold: float = Field(default=0.0, ge=0.0)


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
    table: str = Field(default="rag_chunks", min_length=1)
    embedding_dim: int = Field(default=1536, ge=1)
    distance_metric: str = Field(default="cosine")
    enable_sparse_fields: bool = Field(default=True)
    metadata_jsonb: bool = Field(default=True)


class RerankSettings(BaseModel):
    """Reranker configuration."""

    backend: str = Field(default="cross_encoder")  # none | cross_encoder | llm
    model: str = Field(default="BAAI/bge-reranker-v2-m3")
    max_candidates: int = Field(default=30, ge=1)
    timeout_sec: float = Field(default=10.0, gt=0)
    fallback_to_none: bool = Field(default=True)


class EvaluationSettings(BaseModel):
    """Evaluation pipeline configuration."""

    enabled: bool = Field(default=True)
    backends: list[str] = Field(default_factory=lambda: ["ragas", "custom"])
    golden_test_set: str = Field(default="./data/eval/golden_set.jsonl")
    custom_metrics: list[str] = Field(
        default_factory=lambda: ["hit_rate", "mrr", "ndcg", "groundedness"]
    )


class ObservabilitySettings(BaseModel):
    """Observability / tracing configuration."""

    enabled: bool = Field(default=True)
    sink: str = Field(default="postgres")  # postgres | jsonl | both
    jsonl_mirror_enabled: bool = Field(default=True)
    jsonl_file: str = Field(default="./logs/rag/traces.jsonl")
    # minimal | standard | verbose
    detail_level: str = Field(default="standard")


class MCPSettings(BaseModel):
    """MCP server transport configuration."""

    transport: str = Field(default="stdio")
    protocol_version: str = Field(default="2025-06-18")
    tool_timeout_sec: int = Field(default=60, ge=1)


class PathsSettings(BaseModel):
    """Filesystem path configuration."""

    documents_root: str = Field(default="./data/documents")
    images_root: str = Field(default="./data/images")
    cache_root: str = Field(default="./cache")
    logs_root: str = Field(default="./logs/rag")


# ---------------------------------------------------------------------------
# Top-level settings
# ---------------------------------------------------------------------------


class Settings(BaseModel):
    """Top-level rag-server settings model (DEV_SPEC 5.6 full coverage)."""

    # Legacy top-level fields kept for A4 baseline compat
    app_name: str = Field(default="rag-mcp-server", min_length=1)
    environment: str = Field(default="development", min_length=1)

    # D10: Full 5.6 sections
    app: AppSettings = Field(default_factory=AppSettings)
    llm: LLMSettings
    loader: LoaderSettings = Field(default_factory=LoaderSettings)
    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    vision_llm: VisionLLMSettings = Field(default_factory=VisionLLMSettings)
    splitter: SplitterSettings = Field(default_factory=SplitterSettings)
    retrieval: RetrievalSettings = Field(default_factory=RetrievalSettings)
    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    vector_store: VectorStoreSettings = Field(
        default_factory=VectorStoreSettings)
    rerank: RerankSettings = Field(default_factory=RerankSettings)
    evaluation: EvaluationSettings = Field(default_factory=EvaluationSettings)
    observability: ObservabilitySettings = Field(
        default_factory=ObservabilitySettings)
    mcp: MCPSettings = Field(default_factory=MCPSettings)
    paths: PathsSettings = Field(default_factory=PathsSettings)


# ---------------------------------------------------------------------------
# Semantic validation
# ---------------------------------------------------------------------------


def validate_settings(settings: Settings) -> list[str]:
    """Validate semantic constraints from DEV_SPEC 5.6.4.

    Returns a list of validation error messages. An empty list means the
    configuration is valid.

    Checks performed:
    1. LLM provider required fields (provider, model, api_key non-placeholder).
    2. Azure LLM: endpoint and deployment_name required.
    3. PgVector: backend, table, embedding_dim consistency.
    4. Retrieval / Rerank parameter ranges.
    5. Embedding dim consistency between embedding and vector_store.
    """
    errors: list[str] = []

    # 1. LLM required fields
    if not settings.llm.provider:
        errors.append("llm.provider must not be empty")
    if not settings.llm.model:
        errors.append("llm.model must not be empty")
    if settings.llm.api_key in ("", "replace-me", "your-api-key"):
        errors.append(
            "llm.api_key appears to be a placeholder; set a real key or use "
            "RAG_LLM_API_KEY env var"
        )
    if settings.llm.provider == "azure":
        if not settings.llm.endpoint:
            errors.append("llm.endpoint is required when llm.provider=azure")
        if not settings.llm.deployment_name:
            errors.append(
                "llm.deployment_name is required when llm.provider=azure")

    # 2. VectorStore / PgVector
    if settings.vector_store.backend == "pgvector":
        if not settings.vector_store.table:
            errors.append("vector_store.table must not be empty")
        if settings.vector_store.embedding_dim < 1:
            errors.append("vector_store.embedding_dim must be >= 1")
        if settings.vector_store.embedding_dim != settings.embedding.embedding_dim:
            errors.append(
                f"embedding_dim mismatch: vector_store.embedding_dim="
                f"{settings.vector_store.embedding_dim} but "
                f"embedding.embedding_dim={settings.embedding.embedding_dim}"
            )

    # 3. Retrieval parameter ranges
    if settings.retrieval.dense_top_k < 1:
        errors.append("retrieval.dense_top_k must be >= 1")
    if settings.retrieval.sparse_top_k < 1:
        errors.append("retrieval.sparse_top_k must be >= 1")
    if settings.retrieval.final_top_k > settings.retrieval.dense_top_k:
        errors.append(
            f"retrieval.final_top_k ({settings.retrieval.final_top_k}) should not "
            f"exceed retrieval.dense_top_k ({settings.retrieval.dense_top_k})"
        )

    # 4. Rerank parameter ranges
    if settings.rerank.max_candidates < 1:
        errors.append("rerank.max_candidates must be >= 1")
    if settings.rerank.timeout_sec <= 0:
        errors.append("rerank.timeout_sec must be > 0")

    return errors


_DEFAULT_CONFIG_PATH = Path(__file__).resolve(
).parents[2] / "config" / "settings.yaml"

_ENV_OVERRIDES: tuple[tuple[str, tuple[str, ...], Callable[[str], Any]], ...] = (
    ("RAG_APP_NAME", ("app_name",), str),
    ("RAG_ENVIRONMENT", ("environment",), str),
    # LLM
    ("RAG_LLM_PROVIDER", ("llm", "provider"), str),
    ("RAG_LLM_MODEL", ("llm", "model"), str),
    ("RAG_LLM_API_KEY", ("llm", "api_key"), str),
    ("RAG_LLM_TIMEOUT_SECONDS", ("llm", "timeout_seconds"), int),
    ("RAG_LLM_ENDPOINT", ("llm", "endpoint"), str),
    ("RAG_LLM_API_VERSION", ("llm", "api_version"), str),
    ("RAG_LLM_DEPLOYMENT", ("llm", "deployment_name"), str),
    ("RAG_LLM_BASE_URL", ("llm", "base_url"), str),
    # Embedding
    ("RAG_EMBEDDING_PROVIDER", ("embedding", "provider"), str),
    ("RAG_EMBEDDING_MODEL", ("embedding", "model"), str),
    ("RAG_EMBEDDING_DIM", ("embedding", "embedding_dim"), int),
    # Vision LLM
    ("DASHSCOPE_API_KEY", ("vision_llm", "api_key"), str),
    ("DASHSCOPE_BASE_URL", ("vision_llm", "base_url"), str),
    ("RAG_VISION_PROVIDER", ("vision_llm", "provider"), str),
    # Retrieval
    ("RAG_RETRIEVAL_TOP_K", ("retrieval", "top_k"), int),
    ("RAG_RETRIEVAL_MODE", ("retrieval", "mode"), str),
    ("RAG_RETRIEVAL_FINAL_TOP_K", ("retrieval", "final_top_k"), int),
    # Rerank
    ("RAG_RERANK_BACKEND", ("rerank", "backend"), str),
    # PostgreSQL
    ("PG_HOST", ("postgres", "host"), str),
    ("PG_PORT", ("postgres", "port"), int),
    ("PG_DATABASE", ("postgres", "database"), str),
    ("PG_USER", ("postgres", "user"), str),
    ("PG_PASSWORD", ("postgres", "password"), str),
    # Azure LLM env vars (standard Azure naming)
    ("AZURE_OPENAI_ENDPOINT", ("llm", "endpoint"), str),
    ("AZURE_OPENAI_API_KEY", ("llm", "api_key"), str),
    ("AZURE_OPENAI_DEPLOYMENT", ("llm", "deployment_name"), str),
)


def _read_yaml(config_path: Path) -> dict[str, Any]:
    if not config_path.exists():
        raise FileNotFoundError(f"Settings file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        loaded = yaml.safe_load(f)

    if loaded is None:
        return {}
    if not isinstance(loaded, dict):
        raise ValueError(
            f"Settings file must contain a YAML mapping: {config_path}")

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

    resolved_path = Path(
        config_path) if config_path is not None else _DEFAULT_CONFIG_PATH
    payload = _read_yaml(resolved_path)
    merged = _apply_env_overrides(payload)
    return Settings.model_validate(merged)
