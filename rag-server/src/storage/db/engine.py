"""SQLAlchemy engine creation with connection pool and timeout configuration."""

from __future__ import annotations

from typing import Any

from sqlalchemy import Engine, create_engine

from core.settings import PostgresSettings


def build_engine(pg: PostgresSettings) -> Engine:
	"""Create a SQLAlchemy Engine from PostgresSettings.

	Applies pool_size, pool_timeout, sslmode, and statement_timeout.
	"""
	url = (
		f"postgresql+psycopg2://{pg.user}:{pg.password}"
		f"@{pg.host}:{pg.port}/{pg.database}"
	)

	connect_args: dict[str, Any] = {"sslmode": pg.sslmode}
	options_parts = [f"-csearch_path={pg.schema_name}"]
	if pg.statement_timeout_ms > 0:
		options_parts.append(f"-cstatement_timeout={pg.statement_timeout_ms}")
	connect_args["options"] = " ".join(options_parts)

	return create_engine(
		url,
		pool_size=pg.pool_size,
		pool_timeout=pg.pool_timeout_sec,
		pool_pre_ping=True,
		connect_args=connect_args,
	)
