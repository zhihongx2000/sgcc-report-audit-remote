"""Core data types shared across all RAG pipeline stages.

Note: This file provides the *minimum* set of types required by D5.
Task E1 will expand Document, Chunk and add IngestionResult.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Document:
	"""Represents a parsed document produced by a Loader."""

	text: str
	metadata: dict[str, Any] = field(default_factory=dict)
	id: str = ""
	source: str = ""


@dataclass
class Chunk:
	"""Represents a text chunk produced by a Splitter."""

	text: str
	metadata: dict[str, Any] = field(default_factory=dict)
	source: str = ""
	chunk_index: int = 0
	start_offset: int = 0
	end_offset: int = 0
