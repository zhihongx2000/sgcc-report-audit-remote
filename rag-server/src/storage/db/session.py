"""SQLAlchemy session context manager for rag-server storage."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import Engine
from sqlalchemy.orm import Session


@contextmanager
def get_session(engine: Engine) -> Generator[Session, None, None]:
	"""Yield a SQLAlchemy Session bound to *engine*.

	Commit/rollback is left to the caller. The session is always closed on exit.
	"""
	with Session(engine) as session:
		yield session
