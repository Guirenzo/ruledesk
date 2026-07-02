from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from collections.abc import Iterator

from app.core.config import settings
from app.db.schema import SCHEMA


def connect(database_path: Path | None = None) -> sqlite3.Connection:
    path = database_path or settings.database_path
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


@contextmanager
def session(database_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    connection = connect(database_path)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()


def init_db(database_path: Path | None = None) -> None:
    with session(database_path) as connection:
        connection.executescript(SCHEMA)
