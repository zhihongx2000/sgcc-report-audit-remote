"""Shared pytest setup for sgcc audit backend tests."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

# Ensure tests can import modules from the local src/ tree without install.
if SRC_DIR.exists():
	sys.path.insert(0, str(SRC_DIR))


def pytest_sessionfinish(session, exitstatus: int) -> None:
	"""Keep bootstrap test collection green while scaffold tests are still empty."""
	if exitstatus == 5:
		session.exitstatus = 0
