import sqlite3
import json
from contextlib import contextmanager
from typing import Dict, Any, Generator
from backend.app.config import settings

@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager to yield a database connection.
    Abstracted to support SQLite for development and PostgreSQL for production.
    """
    if settings.db_type == "sqlite":
        conn = sqlite3.connect(settings.db_path)
        # Enable foreign keys and dictionary row factory
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    else:
        # Placeholder for PostgreSQL connection logic in production
        # import psycopg2
        # conn = psycopg2.connect(settings.postgres_dsn)
        # yield conn
        raise NotImplementedError("PostgreSQL database connection is designed but not implemented in Phase 3A.")

def row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    """Helper to convert sqlite3.Row database rows into Python dictionaries with JSON parsing."""
    if not row:
        return {}
    d = dict(row)
    # Parse JSON fields automatically
    json_fields = {
        "provenance_metadata", "normalization", "entity_ids", "custom_fields",
        "tier_breakdown", "work_distribution", "co_occurring_entities", "sample_verse_ids"
    }
    for field in json_fields:
        if field in d and d[field]:
            try:
                d[field] = json.loads(d[field])
            except (json.JSONDecodeError, TypeError):
                pass
    return d
