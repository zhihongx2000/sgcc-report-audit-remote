"""Parent-Child Splitter: convenience wrapper pre-configured for parent-child retrieval.

Provides default chunk sizes suitable for parent-child retrieval patterns
where parents give broad context and children are the indexed units.
"""

from __future__ import annotations

from core.types import Chunk, Document
from ingestion.splitters.recursive_character_splitter import RecursiveCharacterSplitter


class ParentChildSplitter(RecursiveCharacterSplitter):
	"""Pre-configured splitter for parent-child retrieval.

	- ``split()`` returns child-sized chunks (the units stored in the vector index).
	- ``split_parent_child()`` returns structured (parent, [children]) pairs.

	Defaults:
	  - parent_chunk_size = 2000
	  - child_chunk_size  = 400
	  - chunk_overlap     = 50
	"""

	def __init__(
		self,
		*,
		parent_chunk_size: int = 2000,
		child_chunk_size: int = 400,
		chunk_overlap: int = 50,
	) -> None:
		super().__init__(
			chunk_size=child_chunk_size,
			chunk_overlap=chunk_overlap,
		)
		self._parent_chunk_size = parent_chunk_size
		self._child_chunk_size = child_chunk_size
		self._default_overlap = chunk_overlap

	def split(self, doc: Document) -> list[Chunk]:
		"""Return child-sized chunks (stored in vector index)."""
		return super().split(doc)

	def split_parent_child(
		self,
		doc: Document,
		*,
		parent_chunk_size: int | None = None,
		child_chunk_size: int | None = None,
		chunk_overlap: int | None = None,
	) -> list[tuple[Chunk, list[Chunk]]]:
		"""Return (parent_chunk, [child_chunks]) pairs using pre-configured defaults."""
		return super().split_parent_child(
			doc,
			parent_chunk_size=parent_chunk_size or self._parent_chunk_size,
			child_chunk_size=child_chunk_size or self._child_chunk_size,
			chunk_overlap=chunk_overlap if chunk_overlap is not None else self._default_overlap,
		)
