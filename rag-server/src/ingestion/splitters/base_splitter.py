"""Abstract Splitter contract for all text-splitting implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod

from core.types import Chunk, Document


class BaseSplitter(ABC):
	"""Base contract for all Splitter implementations.

	Subclasses must implement ``split``.  ``split_parent_child`` raises
	``NotImplementedError`` unless the subclass overrides it.
	"""

	@abstractmethod
	def split(self, doc: Document) -> list[Chunk]:
		"""Split *doc* into a flat list of Chunks.

		Each returned Chunk must carry:
		  - ``source``       – origin document identifier.
		  - ``chunk_index``  – 0-based sequential position.
		  - ``start_offset`` – character offset into the original text.
		  - ``end_offset``   – exclusive end offset.
		"""

	def split_parent_child(
		self,
		doc: Document,
		*,
		parent_chunk_size: int,
		child_chunk_size: int,
		chunk_overlap: int = 0,
	) -> list[tuple[Chunk, list[Chunk]]]:
		"""Split *doc* into (parent_chunk, [child_chunks]) pairs.

		The parent provides broad context while children are the units
		stored in the vector index.
		"""
		raise NotImplementedError(
			f"{type(self).__name__} does not implement split_parent_child()"
		)
