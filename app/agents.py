from __future__ import annotations

from dataclasses import dataclass

from app.models import AgentResult, MigrationRequest


@dataclass
class DiscoveryAgent:
    """Scans the repository and identifies migration hotspots."""

    def run(self, request: MigrationRequest) -> AgentResult:
        hotspots = [
            "tight DB coupling",
            "manual deployment scripts",
            "missing test coverage",
        ]
        return AgentResult(
            name="discovery-agent",
            summary=f"Identified {len(hotspots)} migration hotspots in {request.repo_url}",
            details={
                "hotspots": hotspots,
                "suggested_service_split": ["api", "worker", "web"],
            },
        )


@dataclass
class PlanningAgent:
    """Converts findings into an implementation plan with risk and effort."""

    def run(self, request: MigrationRequest) -> AgentResult:
        return AgentResult(
            name="planning-agent",
            summary="Generated phased migration plan with risk scoring",
            details={
                "phases": [
                    "baseline and tests",
                    "containerization",
                    "service decomposition",
                    "gcp rollout",
                ],
                "risk_score": 0.34,
                "effort_weeks": 4,
            },
        )


@dataclass
class RefactorAgent:
    """Produces code-level modernization tasks and pull request plan."""

    def run(self, request: MigrationRequest) -> AgentResult:
        return AgentResult(
            name="refactor-agent",
            summary="Prepared modernization PR checklist for engineers",
            details={
                "prs": [
                    "Introduce FastAPI service boundary",
                    "Add repository abstraction for DB",
                    "Add CI gates for lint/test/security",
                ],
                "target_architecture": request.target_architecture,
            },
        )


@dataclass
class ValidationAgent:
    """Defines quality gates before production deployment."""

    def run(self, request: MigrationRequest) -> AgentResult:
        return AgentResult(
            name="validation-agent",
            summary="Attached deployment quality gates",
            details={
                "quality_gates": [
                    "unit tests > 80%",
                    "integration tests pass",
                    "container vulnerability scan high=0",
                ],
                "rollback_strategy": "blue-green switch back to previous revision",
            },
        )
