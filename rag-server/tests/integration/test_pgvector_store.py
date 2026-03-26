"""Integration tests for PgVectorStore.

These tests connect to a live PostgreSQL+pgvector instance.
They are automatically skipped when the database is unreachable.

Required environment variables (defaults from settings.yaml apply):
  PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PASSWORD
"""

from __future__ import annotations

import os
import uuid

import pytest
from sqlalchemy.exc import OperationalError

from core.settings import PostgresSettings
from storage.db.engine import build_engine
from storage.vector.pgvector_store import PgVectorStore
from storage.vector.base_vector_store import VectorRecord

# ---------------------------------------------------------------------------
# Fixture: engine (skips if DB unreachable)
# ---------------------------------------------------------------------------

_TEST_TABLE = "test_rag_chunks_d6"
_DIM = 4  # tiny dimension for test speed


@pytest.fixture(scope="module")
def vector_store():
	"""Build PgVectorStore against a test table; skip if DB is unavailable."""
	pg = PostgresSettings(
		host=os.getenv("PG_HOST", "localhost"),
		port=int(os.getenv("PG_PORT", "5432")),
		database=os.getenv("PG_DATABASE", "rag_db"),
		user=os.getenv("PG_USER", "postgres"),
		password=os.getenv("PG_PASSWORD", ""),
	)
	engine = build_engine(pg)
	try:
		with engine.connect() as conn:
			conn.execute(__import__("sqlalchemy").text("SELECT 1"))
	except OperationalError as exc:
		pytest.skip(f"PostgreSQL not available: {exc}")

	store = PgVectorStore(engine, table=_TEST_TABLE, embedding_dim=_DIM, distance_metric="cosine")
	yield store

	# Teardown: drop test table
	from storage.db.session import get_session
	from sqlalchemy import text

	with get_session(engine) as session:
		session.execute(text(f"DROP TABLE IF EXISTS {_TEST_TABLE}"))
		session.commit()
	engine.dispose()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_record(
	source: str = "test.pdf",
	vec: list[float] | None = None,
	extra_meta: dict | None = None,
) -> VectorRecord:
	return VectorRecord(
		id=str(uuid.uuid4()),
		text=f"chunk from {source}",
		dense_vector=vec or [0.1, 0.2, 0.3, 0.4],
		metadata={"source": source, **(extra_meta or {})},
	)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestPgVectorStoreUpsertAndQuery:
	def test_upsert_returns_correct_count(self, vector_store: PgVectorStore) -> None:
		records = [_make_record() for _ in range(3)]
		count = vector_store.upsert(records)
		assert count == 3

	def test_upsert_idempotent_on_same_id(self, vector_store: PgVectorStore) -> None:
		rec = _make_record(source="idem.pdf", vec=[1.0, 0.0, 0.0, 0.0])
		vector_store.upsert([rec])
		# Upsert the same id with changed text – should not raise or duplicate
		rec_updated = VectorRecord(
			id=rec.id,
			text="updated content",
			dense_vector=[1.0, 0.0, 0.0, 0.0],
			metadata=rec.metadata,
		)
		count = vector_store.upsert([rec_updated])
		assert count == 1

	def test_query_returns_results(self, vector_store: PgVectorStore) -> None:
		rec = _make_record(source="query_test.pdf", vec=[0.9, 0.1, 0.0, 0.0])
		vector_store.upsert([rec])

		results = vector_store.query([0.9, 0.1, 0.0, 0.0], top_k=5)
		assert len(results) >= 1
		ids = [r.id for r in results]
		assert rec.id in ids

	def test_query_scores_between_minus1_and_1(self, vector_store: PgVectorStore) -> None:
		rec = _make_record(vec=[0.5, 0.5, 0.0, 0.0])
		vector_store.upsert([rec])
		results = vector_store.query([0.5, 0.5, 0.0, 0.0], top_k=3)
		for r in results:
			assert -1.0 <= r.score <= 1.0 + 1e-6

	def test_query_with_metadata_filter(self, vector_store: PgVectorStore) -> None:
		src_a = f"a_{uuid.uuid4().hex[:6]}.pdf"
		src_b = f"b_{uuid.uuid4().hex[:6]}.pdf"
		rec_a = _make_record(source=src_a, vec=[1.0, 0.0, 0.0, 0.0])
		rec_b = _make_record(source=src_b, vec=[1.0, 0.0, 0.0, 0.0])
		vector_store.upsert([rec_a, rec_b])

		results = vector_store.query(
			[1.0, 0.0, 0.0, 0.0],
			top_k=10,
			metadata_filter={"source": src_a},
		)
		returned_ids = {r.id for r in results}
		assert rec_a.id in returned_ids
		assert rec_b.id not in returned_ids

	def test_delete_by_metadata(self, vector_store: PgVectorStore) -> None:
		src = f"del_{uuid.uuid4().hex[:6]}.pdf"
		recs = [_make_record(source=src) for _ in range(2)]
		vector_store.upsert(recs)

		deleted = vector_store.delete({"source": src})
		assert deleted == 2

		# Verify records are gone
		remaining = vector_store.get_by_metadata({"source": src})
		assert remaining == []

	def test_delete_empty_filter_raises(self, vector_store: PgVectorStore) -> None:
		with pytest.raises(ValueError, match="metadata_filter must not be empty"):
			vector_store.delete({})

	def test_get_all_returns_list(self, vector_store: PgVectorStore) -> None:
		result = vector_store.get_all()
		assert isinstance(result, list)

	def test_get_by_metadata_filters_correctly(self, vector_store: PgVectorStore) -> None:
		src = f"browse_{uuid.uuid4().hex[:6]}.pdf"
		rec = _make_record(source=src)
		vector_store.upsert([rec])

		found = vector_store.get_by_metadata({"source": src})
		assert len(found) == 1
		assert found[0].id == rec.id
		assert found[0].text == rec.text
