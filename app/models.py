from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MigrationStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class MigrationRequest(BaseModel):
    repo_url: str = Field(..., description="Git repository URL for the legacy application")
    language: str = Field(..., description="Primary language in the repository")
    target_architecture: str = Field(
        default="cloud-run-microservices", description="Target architecture pattern"
    )


class AgentResult(BaseModel):
    name: str
    summary: str
    details: dict[str, Any]


class MigrationRecord(BaseModel):
    migration_id: str
    created_at: datetime
    status: MigrationStatus
    request: MigrationRequest
    results: list[AgentResult] = Field(default_factory=list)
    rollout_steps: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str
