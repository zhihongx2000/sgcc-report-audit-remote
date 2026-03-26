"""Abstract VectorStore interface for all vector storage backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class VectorRecord:
	"""A single record stored in the vector store."""

	id: str
	text: str
	dense_vector: list[float]
	sparse_vector: dict[str, float] | None = None
	metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryResult:
	"""A retrieval result with similarity score."""

	id: str
	text: str
	score: float
	metadata: dict[str, Any] = field(default_factory=dict)


class BaseVectorStore(ABC):
	"""Abstract interface for all vector store backends.

	All implementations must support:
	  - ``upsert()``  – idempotent batch write
	  - ``query()``   – similarity search with optional metadata filter
	  - ``delete()``  – remove records matching a metadata filter
	"""

	@abstractmethod
	def upsert(self, records: list[VectorRecord]) -> int:
		"""Upsert *records* into the store.

		Returns the number of records written. Conflicts on ``id`` are resolved
		by overwriting the existing row.
		"""

	@abstractmethod
	def query(
		self,
		dense_vector: list[float],
		*,
		top_k: int = 10,
		metadata_filter: dict[str, Any] | None = None,
	) -> list[QueryResult]:
		"""Return the *top_k* records nearest to *dense_vector*.

		*metadata_filter* is an optional exact-match filter on top-level JSONB
		keys (e.g. ``{"source": "report.pdf"}``).  All filter entries must match.
		"""

	@abstractmethod
	def delete(self, metadata_filter: dict[str, Any]) -> int:
		"""Delete all records whose metadata contains *metadata_filter* keys.

		Returns the number of rows deleted.
		"""

	def get_all(self) -> list[VectorRecord]:
		"""Return all records in the store (default: not implemented)."""
		raise NotImplementedError(
			f"{type(self).__name__} does not implement get_all()"
		)

	def get_by_metadata(self, metadata_filter: dict[str, Any]) -> list[VectorRecord]:
		"""Return records matching *metadata_filter* (default: not implemented)."""
		raise NotImplementedError(
			f"{type(self).__name__} does not implement get_by_metadata()"
		)
