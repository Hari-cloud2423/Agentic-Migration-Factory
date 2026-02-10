from __future__ import annotations

from app.agents import DiscoveryAgent, PlanningAgent, RefactorAgent, ValidationAgent
from app.models import MigrationRequest


class MigrationPipeline:
    def __init__(self) -> None:
        self.discovery = DiscoveryAgent()
        self.planning = PlanningAgent()
        self.refactor = RefactorAgent()
        self.validation = ValidationAgent()

    def execute(self, request: MigrationRequest):
        return [
            self.discovery.run(request),
            self.planning.run(request),
            self.refactor.run(request),
            self.validation.run(request),
        ]
