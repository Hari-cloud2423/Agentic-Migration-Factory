from __future__ import annotations

import logging
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request

from app.config import settings
from app.models import HealthResponse, MigrationRecord, MigrationRequest, MigrationStatus
from app.pipeline import MigrationPipeline
from app.storage import InMemoryMigrationStore, MigrationStore, SqliteMigrationStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def build_store() -> MigrationStore:
    if settings.store_backend.lower() == "sqlite":
        logger.info("Using sqlite migration store at %s", settings.sqlite_path)
        return SqliteMigrationStore(settings.sqlite_path)
    logger.info("Using in-memory migration store")
    return InMemoryMigrationStore()


app = FastAPI(title=settings.app_name, version=settings.app_version)
store = build_store()
pipeline = MigrationPipeline()


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid4())
    logger.info("request.start id=%s method=%s path=%s", request_id, request.method, request.url.path)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    logger.info("request.end id=%s status=%s", request_id, response.status_code)
    return response


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=settings.app_name)


@app.post("/migrations", response_model=MigrationRecord, status_code=201)
def create_migration(request: MigrationRequest) -> MigrationRecord:
    migration_id = str(uuid4())
    record = MigrationRecord(
        migration_id=migration_id,
        created_at=datetime.now(timezone.utc),
        status=MigrationStatus.running,
        request=request,
    )
    store.save(record)

    try:
        results = pipeline.execute(request)
        record.results = results
        record.status = MigrationStatus.completed
        record.rollout_steps = [
            "Build container image and push to Artifact Registry",
            "Deploy canary revision to Cloud Run",
            "Run smoke tests via Cloud Build",
            "Promote traffic to 100%",
        ]
    except Exception as exc:  # pragma: no cover
        logger.exception("migration.failed id=%s", migration_id)
        record.status = MigrationStatus.failed
        record.rollout_steps = [f"Pipeline failed: {exc}"]

    store.save(record)
    return record


@app.get("/migrations", response_model=list[MigrationRecord])
def list_migrations() -> list[MigrationRecord]:
    return store.list()


@app.get("/migrations/{migration_id}", response_model=MigrationRecord)
def get_migration(migration_id: str) -> MigrationRecord:
    record = store.get(migration_id)
    if not record:
        raise HTTPException(status_code=404, detail="Migration not found")
    return record
