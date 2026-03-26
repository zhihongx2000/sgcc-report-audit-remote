"""LangChain RecursiveCharacterTextSplitter-based Splitter implementation.

Uses Markdown-aware separators to produce semantically coherent chunks.
"""

from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.types import Chunk, Document
from ingestion.splitters.base_splitter import BaseSplitter

# Markdown structural separators in descending priority order.
_MARKDOWN_SEPARATORS: list[str] = [
	"\n## ",
	"\n### ",
	"\n#### ",
	"\n\n",
	"\n",
	" ",
	"",
]


class RecursiveCharacterSplitter(BaseSplitter):
	"""Wraps LangChain's RecursiveCharacterTextSplitter with Markdown separators.

	All Chunk objects produced contain ``source``, ``chunk_index``,
	``start_offset`` and ``end_offset`` fields as required by the spec.
	"""

	def __init__(
		self,
		*,
		chunk_size: int = 1000,
		chunk_overlap: int = 200,
		separators: list[str] | None = None,
	) -> None:
		self._chunk_size = chunk_size
		self._chunk_overlap = chunk_overlap
		self._separators = separators or _MARKDOWN_SEPARATORS

	def _build_lc_splitter(
		self,
		*,
		chunk_size: int,
		chunk_overlap: int,
	) -> RecursiveCharacterTextSplitter:
		return RecursiveCharacterTextSplitter(
			chunk_size=chunk_size,
			chunk_overlap=chunk_overlap,
			separators=self._separators,
			keep_separator=True,
			add_start_index=True,
			strip_whitespace=True,
		)

	def split(self, doc: Document) -> list[Chunk]:
		"""Split *doc.text* into chunks using RecursiveCharacterTextSplitter."""
		source = doc.source or doc.id
		lc_splitter = self._build_lc_splitter(
			chunk_size=self._chunk_size,
			chunk_overlap=self._chunk_overlap,
		)
		lc_docs = lc_splitter.create_documents(
			[doc.text],
			metadatas=[{"source": source, **doc.metadata}],
		)
		chunks: list[Chunk] = []
		for idx, lc_doc in enumerate(lc_docs):
			start = lc_doc.metadata.pop("start_index", 0)
			text = lc_doc.page_content
			chunks.append(
				Chunk(
					text=text,
					metadata=dict(lc_doc.metadata),
					source=source,
					chunk_index=idx,
					start_offset=start,
					end_offset=start + len(text),
				)
			)
		return chunks

	def split_parent_child(
		self,
		doc: Document,
		*,
		parent_chunk_size: int,
		child_chunk_size: int,
		chunk_overlap: int = 0,
	) -> list[tuple[Chunk, list[Chunk]]]:
		"""Split *doc* into (parent_chunk, [child_chunks]) pairs.

		Each parent is first split from the full document, then each parent text
		is independently split into child chunks.  Child ``start_offset`` and
		``end_offset`` are relative to the *original* document text.
		"""
		source = doc.source or doc.id
		parent_lc = self._build_lc_splitter(
			chunk_size=parent_chunk_size,
			chunk_overlap=chunk_overlap,
		)
		child_lc = self._build_lc_splitter(
			chunk_size=child_chunk_size,
			chunk_overlap=chunk_overlap,
		)

		parent_lc_docs = parent_lc.create_documents(
			[doc.text],
			metadatas=[{"source": source, **doc.metadata}],
		)

		result: list[tuple[Chunk, list[Chunk]]] = []
		for parent_idx, parent_lc_doc in enumerate(parent_lc_docs):
			parent_start: int = parent_lc_doc.metadata.pop("start_index", 0)
			parent_text = parent_lc_doc.page_content
			parent_chunk = Chunk(
				text=parent_text,
				metadata=dict(parent_lc_doc.metadata),
				source=source,
				chunk_index=parent_idx,
				start_offset=parent_start,
				end_offset=parent_start + len(parent_text),
			)

			# Split the parent text into children; offsets are relative to parent.
			child_lc_docs = child_lc.create_documents(
				[parent_text],
				metadatas=[{"source": source, "parent_index": parent_idx}],
			)
			children: list[Chunk] = []
			for child_idx, child_lc_doc in enumerate(child_lc_docs):
				rel_start: int = child_lc_doc.metadata.pop("start_index", 0)
				child_text = child_lc_doc.page_content
				children.append(
					Chunk(
						text=child_text,
						metadata=dict(child_lc_doc.metadata),
						source=source,
						chunk_index=child_idx,
						start_offset=parent_start + rel_start,
						end_offset=parent_start + rel_start + len(child_text),
					)
				)
			result.append((parent_chunk, children))

		return result
