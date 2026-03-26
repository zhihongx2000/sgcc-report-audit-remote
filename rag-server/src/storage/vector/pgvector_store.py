"""PgVector implementation of BaseVectorStore using SQLAlchemy + pgvector."""

from __future__ import annotations

import json
import logging
from typing import Any

from sqlalchemy import Engine, text

from storage.db.session import get_session
from storage.vector.base_vector_store import (
	BaseVectorStore,
	QueryResult,
	VectorRecord,
)

logger = logging.getLogger(__name__)

# Distance operator per metric (pgvector SQL operators)
_DISTANCE_OPS: dict[str, str] = {
	"cosine": "<=>",
	"l2": "<->",
	"inner_product": "<#>",
}

# Index ops class per metric (used when creating HNSW index)
_INDEX_OPS: dict[str, str] = {
	"cosine": "vector_cosine_ops",
	"l2": "vector_l2_ops",
	"inner_product": "vector_ip_ops",
}


class PgVectorStore(BaseVectorStore):
	"""Vector store backed by PostgreSQL + pgvector extension.

	Supports:
	  - Idempotent ``upsert()`` via ``ON CONFLICT (id) DO UPDATE``.
	  - Similarity ``query()`` with optional JSONB metadata filter.
	  - ``delete()`` by metadata JSONB containment.
	  - ``get_all()`` and ``get_by_metadata()`` for data browsing.
	"""

	def __init__(
		self,
		engine: Engine,
		*,
		table: str = "rag_chunks",
		embedding_dim: int = 1536,
		distance_metric: str = "cosine",
	) -> None:
		if distance_metric not in _DISTANCE_OPS:
			raise ValueError(
				f"Unsupported distance_metric={distance_metric!r}. "
				f"Choose from: {sorted(_DISTANCE_OPS)}"
			)
		self._engine = engine
		self._table = table
		self._embedding_dim = embedding_dim
		self._distance_metric = distance_metric
		self._dist_op = _DISTANCE_OPS[distance_metric]
		self._ensure_table()

	# ------------------------------------------------------------------
	# Schema bootstrap
	# ------------------------------------------------------------------

	def _ensure_table(self) -> None:
		"""Create pgvector extension and rag_chunks table if absent."""
		with get_session(self._engine) as session:
			session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
			session.execute(
				text(f"""
					CREATE TABLE IF NOT EXISTS {self._table} (
						id            TEXT PRIMARY KEY,
						content       TEXT        NOT NULL,
						dense_vector  vector({self._embedding_dim}),
						sparse_vector JSONB,
						metadata      JSONB        NOT NULL DEFAULT '{{}}'
					)
				""")
			)
			# HNSW index supports empty tables (unlike ivfflat which needs data)
			idx_ops = _INDEX_OPS[self._distance_metric]
			session.execute(
				text(f"""
					CREATE INDEX IF NOT EXISTS {self._table}_dense_vec_hnsw_idx
					ON {self._table}
					USING hnsw (dense_vector {idx_ops})
				""")
			)
			session.commit()
		logger.debug("PgVectorStore initialized: table=%s dim=%d", self._table, self._embedding_dim)

	# ------------------------------------------------------------------
	# BaseVectorStore contract
	# ------------------------------------------------------------------

	def upsert(self, records: list[VectorRecord]) -> int:
		"""Idempotent batch upsert. Returns number of rows upserted."""
		if not records:
			return 0

		rows: list[dict[str, Any]] = []
		for r in records:
			vec_str = "[" + ",".join(str(v) for v in r.dense_vector) + "]"
			rows.append(
				{
					"id": r.id,
					"content": r.text,
					"dense_vector": vec_str,
					"sparse_vector": json.dumps(r.sparse_vector) if r.sparse_vector is not None else None,
					"metadata": json.dumps(r.metadata),
				}
			)

		with get_session(self._engine) as session:
			for row in rows:
				session.execute(
					text(f"""
						INSERT INTO {self._table}
							(id, content, dense_vector, sparse_vector, metadata)
						VALUES (
							:id,
							:content,
							CAST(:dense_vector AS vector),
							CAST(:sparse_vector AS jsonb),
							CAST(:metadata AS jsonb)
						)
						ON CONFLICT (id) DO UPDATE SET
							content       = EXCLUDED.content,
							dense_vector  = EXCLUDED.dense_vector,
							sparse_vector = EXCLUDED.sparse_vector,
							metadata      = EXCLUDED.metadata
					"""),
					row,
				)
			session.commit()

		logger.debug("Upserted %d records into %s", len(records), self._table)
		return len(records)

	def query(
		self,
		dense_vector: list[float],
		*,
		top_k: int = 10,
		metadata_filter: dict[str, Any] | None = None,
	) -> list[QueryResult]:
		"""Return top_k nearest records ordered by distance.

		When *metadata_filter* is provided, only records whose ``metadata``
		JSONB contains all key/value pairs from the filter are returned.
		"""
		vec_str = "[" + ",".join(str(v) for v in dense_vector) + "]"

		if metadata_filter:
			filter_clause = "WHERE metadata @> CAST(:filter AS jsonb)"
			params: dict[str, Any] = {
				"vec": vec_str,
				"top_k": top_k,
				"filter": json.dumps(metadata_filter),
			}
		else:
			filter_clause = ""
			params = {"vec": vec_str, "top_k": top_k}

		# For cosine distance: score = 1 - distance (higher is more similar)
		# For L2/inner_product: score = -distance (negated so higher is better)
		if self._distance_metric == "cosine":
			score_expr = f"1 - (dense_vector {self._dist_op} CAST(:vec AS vector))"
		else:
			score_expr = f"-(dense_vector {self._dist_op} CAST(:vec AS vector))"

		sql = text(f"""
			SELECT id, content, metadata, {score_expr} AS score
			FROM {self._table}
			{filter_clause}
			ORDER BY dense_vector {self._dist_op} CAST(:vec AS vector)
			LIMIT :top_k
		""")

		with get_session(self._engine) as session:
			rows = session.execute(sql, params).fetchall()

		return [
			QueryResult(
				id=row.id,
				text=row.content,
				score=float(row.score),
				metadata=row.metadata or {},
			)
			for row in rows
		]

	def delete(self, metadata_filter: dict[str, Any]) -> int:
		"""Delete all records whose metadata JSONB contains *metadata_filter*.

		Returns the number of rows deleted.
		"""
		if not metadata_filter:
			raise ValueError("metadata_filter must not be empty to prevent accidental full-table deletion")

		with get_session(self._engine) as session:
			result = session.execute(
				text(f"DELETE FROM {self._table} WHERE metadata @> CAST(:filter AS jsonb)"),
				{"filter": json.dumps(metadata_filter)},
			)
			session.commit()
			return result.rowcount  # type: ignore[return-value]

	# ------------------------------------------------------------------
	# Data browsing helpers
	# ------------------------------------------------------------------

	def get_all(self) -> list[VectorRecord]:
		"""Return all records (dense_vector excluded for performance)."""
		with get_session(self._engine) as session:
			rows = session.execute(
				text(f"SELECT id, content, sparse_vector, metadata FROM {self._table}")
			).fetchall()

		return [
			VectorRecord(
				id=row.id,
				text=row.content,
				dense_vector=[],
				sparse_vector=row.sparse_vector,
				metadata=row.metadata or {},
			)
			for row in rows
		]

	def get_by_metadata(self, metadata_filter: dict[str, Any]) -> list[VectorRecord]:
		"""Return records matching *metadata_filter* containment."""
		with get_session(self._engine) as session:
			rows = session.execute(
				text(
					f"SELECT id, content, sparse_vector, metadata "
					f"FROM {self._table} WHERE metadata @> CAST(:filter AS jsonb)"
				),
				{"filter": json.dumps(metadata_filter)},
			).fetchall()

		return [
			VectorRecord(
				id=row.id,
				text=row.content,
				dense_vector=[],
				sparse_vector=row.sparse_vector,
				metadata=row.metadata or {},
			)
			for row in rows
		]
