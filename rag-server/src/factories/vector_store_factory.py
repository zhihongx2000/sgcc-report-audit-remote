"""Factory for creating VectorStore instances from configuration."""

from __future__ import annotations

from sqlalchemy import Engine

from core.settings import VectorStoreSettings
from storage.vector.base_vector_store import BaseVectorStore
from storage.vector.pgvector_store import PgVectorStore


def create_vector_store(
    settings: VectorStoreSettings,
    *,
    engine: Engine,
) -> BaseVectorStore:
    """Instantiate a VectorStore from *settings*.

    Args:
        settings: VectorStore settings section from the application config.
        engine: SQLAlchemy :class:`Engine` to connect to the database.

    Returns:
        A concrete :class:`BaseVectorStore` instance.

    Raises:
        ValueError: If *settings.backend* is not a registered backend.
    """
    backend = settings.backend.lower().strip()

    if backend == "pgvector":
        return PgVectorStore(
            engine,
            table=settings.table,
            embedding_dim=settings.embedding_dim,
            distance_metric=settings.distance_metric,
        )
    raise ValueError(
        f"Unknown vector store backend '{settings.backend}'. "
        "Available backends: pgvector"
    )
