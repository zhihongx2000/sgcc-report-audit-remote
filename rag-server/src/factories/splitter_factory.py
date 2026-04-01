"""Factory for creating Splitter instances from configuration."""

from __future__ import annotations

from ingestion.splitters.base_splitter import BaseSplitter
from ingestion.splitters.parent_child_splitter import ParentChildSplitter
from ingestion.splitters.recursive_character_splitter import (
    RecursiveCharacterSplitter,
)


def create_splitter(splitter_type: str, **kwargs) -> BaseSplitter:  # noqa: ANN003
    """Instantiate a Splitter by *splitter_type* name.

    Args:
        splitter_type: Splitter type identifier (``"recursive_character"`` or
            ``"parent_child"``).  
        **kwargs: Forwarded to the splitter constructor:
            - ``recursive_character``: ``chunk_size``, ``chunk_overlap``.
            - ``parent_child``: ``parent_chunk_size``, ``child_chunk_size``,
              ``chunk_overlap``.

    Returns:
        A concrete :class:`BaseSplitter` instance.

    Raises:
        ValueError: If *splitter_type* is not a registered type.
    """
    _type = splitter_type.lower().strip()

    if _type == "recursive_character":
        return RecursiveCharacterSplitter(
            chunk_size=int(kwargs.get("chunk_size", 1000)),
            chunk_overlap=int(kwargs.get("chunk_overlap", 200)),
        )
    if _type == "parent_child":
        return ParentChildSplitter(
            parent_chunk_size=int(kwargs.get("parent_chunk_size", 2000)),
            child_chunk_size=int(kwargs.get("child_chunk_size", 400)),
            chunk_overlap=int(kwargs.get("chunk_overlap", 50)),
        )
    raise ValueError(
        f"Unknown splitter type '{splitter_type}'. "
        "Available types: parent_child, recursive_character"
    )
