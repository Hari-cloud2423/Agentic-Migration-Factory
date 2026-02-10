from datetime import datetime, timezone

import pytest

pytest.importorskip("pydantic")

from app.models import MigrationRecord, MigrationRequest, MigrationStatus
from app.storage import SqliteMigrationStore


def test_sqlite_store_roundtrip(tmp_path):
    db_path = tmp_path / "store.db"
    store = SqliteMigrationStore(str(db_path))

    record = MigrationRecord(
        migration_id="mig-1",
        created_at=datetime.now(timezone.utc),
        status=MigrationStatus.completed,
        request=MigrationRequest(repo_url="https://github.com/example/legacy", language="python"),
        rollout_steps=["step1"],
    )

    store.save(record)
    fetched = store.get("mig-1")

    assert fetched is not None
    assert fetched.migration_id == "mig-1"
    assert fetched.status == MigrationStatus.completed

    all_rows = store.list()
    assert len(all_rows) == 1
