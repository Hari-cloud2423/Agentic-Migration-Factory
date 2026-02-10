from __future__ import annotations

import sqlite3
from abc import ABC, abstractmethod
from threading import Lock

from app.models import MigrationRecord


class MigrationStore(ABC):
    @abstractmethod
    def save(self, record: MigrationRecord) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, migration_id: str) -> MigrationRecord | None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[MigrationRecord]:
        raise NotImplementedError


class InMemoryMigrationStore(MigrationStore):
    def __init__(self) -> None:
        self._data: dict[str, MigrationRecord] = {}
        self._lock = Lock()

    def save(self, record: MigrationRecord) -> None:
        with self._lock:
            self._data[record.migration_id] = record

    def get(self, migration_id: str) -> MigrationRecord | None:
        with self._lock:
            return self._data.get(migration_id)

    def list(self) -> list[MigrationRecord]:
        with self._lock:
            return list(self._data.values())


class SqliteMigrationStore(MigrationStore):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._lock = Lock()
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS migrations (
                    migration_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def save(self, record: MigrationRecord) -> None:
        payload = record.model_dump_json()
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO migrations (migration_id, payload, created_at)
                    VALUES (?, ?, ?)
                    ON CONFLICT(migration_id) DO UPDATE SET payload=excluded.payload
                    """,
                    (record.migration_id, payload, record.created_at.isoformat()),
                )
                conn.commit()

    def get(self, migration_id: str) -> MigrationRecord | None:
        with self._lock:
            with self._connect() as conn:
                row = conn.execute(
                    "SELECT payload FROM migrations WHERE migration_id = ?",
                    (migration_id,),
                ).fetchone()
        if not row:
            return None
        return MigrationRecord.model_validate_json(row["payload"])

    def list(self) -> list[MigrationRecord]:
        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    "SELECT payload FROM migrations ORDER BY created_at DESC"
                ).fetchall()
        return [MigrationRecord.model_validate_json(row["payload"]) for row in rows]
