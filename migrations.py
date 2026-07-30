"""Idempotent schema entrypoint. Safe to run more than once.

Usage: uv run python migrations.py
"""

import logging

import app.models  # noqa: F401  (import registers every table on Base.metadata)
from app.db.session import get_engine
from app.logging_config import configure_logging
from app.models.base import Base

logger = logging.getLogger(__name__)


def run() -> None:
    engine = get_engine()

    Base.metadata.create_all(engine, checkfirst=True)
    logger.info("Schema is up to date.")

    # --- Ad-hoc section -----------------------------------------------
    # One-off ALTERs go here, guarded so they're safe to re-run
    # (e.g. `ADD COLUMN IF NOT EXISTS`). Clear this section once applied
    # everywhere — git history is the record, not this file.
    # --------------------------------------------------------------------


if __name__ == "__main__":
    configure_logging()
    run()
