"""Unit tests for RecursiveCharacterSplitter and ParentChildSplitter.

Validates:
  - split() returns correct chunk count, sequential indices, and valid offsets.
  - split_parent_child() returns well-formed (parent, [children]) pairs.
"""

from __future__ import annotations

import pytest

from core.types import Document
from ingestion.splitters.parent_child_splitter import ParentChildSplitter
from ingestion.splitters.recursive_character_splitter import RecursiveCharacterSplitter

# ---------------------------------------------------------------------------
# Sample text (Markdown structure that exercises heading-based separators)
# ---------------------------------------------------------------------------
SAMPLE_TEXT = """\
## Section 1

This is the first paragraph of section one. It contains meaningful text
that should ideally not be cut in the middle of a sentence.

## Section 2

This is the second section with different content. It also has multiple
paragraphs that should be respected during splitting.

### Subsection 2.1

A subsection with more detailed information about the second section topic.

## Section 3

Final section with additional content to ensure the splitter produces
at least a few chunks when using a small chunk_size.
"""


def _make_doc(source: str = "test_doc.md", text: str = SAMPLE_TEXT) -> Document:
	return Document(text=text, source=source)


# ===========================================================================
# RecursiveCharacterSplitter
# ===========================================================================


class TestRecursiveCharacterSplitter:
	def test_split_returns_at_least_one_chunk(self) -> None:
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(_make_doc())
		assert len(chunks) >= 1

	def test_chunk_index_is_sequential(self) -> None:
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(_make_doc())
		assert [c.chunk_index for c in chunks] == list(range(len(chunks)))

	def test_chunk_source_matches_document(self) -> None:
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(_make_doc(source="my_report.pdf"))
		assert all(c.source == "my_report.pdf" for c in chunks)

	def test_end_offset_greater_than_start(self) -> None:
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(_make_doc())
		for chunk in chunks:
			assert chunk.end_offset > chunk.start_offset

	def test_offsets_within_original_text_bounds(self) -> None:
		doc = _make_doc()
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(doc)
		for chunk in chunks:
			assert chunk.start_offset >= 0
			assert chunk.end_offset <= len(doc.text) + 5  # allow 5-char tolerance for strip

	def test_smaller_chunk_size_yields_more_chunks(self) -> None:
		doc = _make_doc()
		large_splitter = RecursiveCharacterSplitter(chunk_size=2000, chunk_overlap=0)
		small_splitter = RecursiveCharacterSplitter(chunk_size=100, chunk_overlap=0)
		assert len(small_splitter.split(doc)) >= len(large_splitter.split(doc))

	def test_content_preserved_across_chunks(self) -> None:
		"""All critical keywords from the original text should appear in chunks."""
		doc = _make_doc()
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=0)
		chunks = splitter.split(doc)
		combined = " ".join(c.text for c in chunks)
		for keyword in ["Section 1", "Section 2", "Subsection 2.1", "Section 3"]:
			assert keyword in combined

	def test_chunk_text_non_empty(self) -> None:
		splitter = RecursiveCharacterSplitter(chunk_size=200, chunk_overlap=20)
		chunks = splitter.split(_make_doc())
		assert all(len(c.text) > 0 for c in chunks)

	def test_large_chunk_size_produces_single_chunk(self) -> None:
		doc = _make_doc()
		splitter = RecursiveCharacterSplitter(chunk_size=10000, chunk_overlap=0)
		chunks = splitter.split(doc)
		assert len(chunks) == 1
		assert chunks[0].chunk_index == 0


# ===========================================================================
# ParentChildSplitter
# ===========================================================================


class TestParentChildSplitter:
	def test_split_parent_child_returns_pairs(self) -> None:
		splitter = ParentChildSplitter(
			parent_chunk_size=500, child_chunk_size=100, chunk_overlap=0
		)
		pairs = splitter.split_parent_child(_make_doc())
		assert len(pairs) >= 1
		for parent, children in pairs:
			assert parent.text
			assert len(children) >= 1

	def test_parent_text_longer_than_each_child(self) -> None:
		splitter = ParentChildSplitter(
			parent_chunk_size=500, child_chunk_size=100, chunk_overlap=0
		)
		pairs = splitter.split_parent_child(_make_doc())
		for parent, children in pairs:
			assert len(parent.text) >= max(len(c.text) for c in children)

	def test_child_source_matches_document(self) -> None:
		splitter = ParentChildSplitter(
			parent_chunk_size=500, child_chunk_size=100, chunk_overlap=0
		)
		pairs = splitter.split_parent_child(_make_doc(source="pc_doc.md"))
		for _, children in pairs:
			assert all(c.source == "pc_doc.md" for c in children)

	def test_child_chunk_index_sequential_within_parent(self) -> None:
		splitter = ParentChildSplitter(
			parent_chunk_size=500, child_chunk_size=100, chunk_overlap=0
		)
		pairs = splitter.split_parent_child(_make_doc())
		for _, children in pairs:
			assert [c.chunk_index for c in children] == list(range(len(children)))

	def test_child_start_offset_within_parent_range(self) -> None:
		splitter = ParentChildSplitter(
			parent_chunk_size=500, child_chunk_size=100, chunk_overlap=0
		)
		pairs = splitter.split_parent_child(_make_doc())
		for parent, children in pairs:
			for child in children:
				assert child.start_offset >= parent.start_offset

	def test_split_returns_child_sized_chunks(self) -> None:
		"""split() should return child-sized (not parent-sized) chunks."""
		doc = _make_doc()
		splitter = ParentChildSplitter(
			parent_chunk_size=2000, child_chunk_size=100, chunk_overlap=0
		)
		child_chunks = splitter.split(doc)
		# With chunk_size=100, all chunks should be ≤ ~200 chars (splitter tolerance)
		assert all(len(c.text) <= 200 for c in child_chunks)

	def test_default_sizes_produce_valid_splits(self) -> None:
		"""Default constructor should work without explicit sizes."""
		splitter = ParentChildSplitter()
		pairs = splitter.split_parent_child(_make_doc())
		assert len(pairs) >= 1
