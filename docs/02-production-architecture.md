# 02 — Production Architecture

## High-level architecture

```text
[Web UI] -> [API Gateway] -> [Orchestrator Service]
                             |-> [Repo Ingestion Agent]
                             |-> [Code Graph Agent]
                             |-> [Migration Strategy Agent]
                             |-> [Transformation Agent]
                             |-> [Validation Agent]
                             |-> [Security/Compliance Agent]
                             |-> [PR & Deployment Agent]

[Metadata DB] [Object Storage] [Queue/Event Bus] [Observability Stack]
```

## Recommended GCP stack
- **Frontend**: Next.js on Cloud Run.
- **Backend API + Orchestrator**: Python FastAPI on Cloud Run.
- **Async tasks**: Cloud Tasks / Pub/Sub workers.
- **State**: Cloud SQL (PostgreSQL).
- **Artifacts**: Cloud Storage.
- **Secrets**: Secret Manager.
- **Identity**: Firebase Auth or Identity Platform.
- **CI/CD**: Cloud Build + GitHub Actions.
- **Monitoring**: Cloud Logging, Cloud Monitoring, Error Reporting.

## Agent responsibilities

### 1) Repo Ingestion Agent
- Clones/imports repository.
- Extracts languages, frameworks, package managers.
- Builds file inventory and baseline metrics.

### 2) Code Graph Agent
- Generates dependency graph and service boundaries.
- Detects anti-patterns (god modules, cyclic deps, hardcoded configs).

### 3) Migration Strategy Agent
- Creates phased migration plan:
  - Rehost / replatform / refactor / rewrite recommendations.
- Provides effort, risk, and confidence scores.

### 4) Transformation Agent
- Produces concrete code changes.
- Applies framework upgrades, modularization, API extraction.
- Writes migration notes for each modified file.

### 5) Validation Agent
- Runs unit/integration tests.
- Runs linting/static analysis.
- Produces migration quality report and diff summary.

### 6) Security & Compliance Agent
- Secret leak checks.
- Dependency vulnerability scanning.
- Policy checks (license/compliance guardrails).

### 7) PR & Deployment Agent
- Opens PRs with rationale and risk notes.
- Generates Cloud Run deploy config and rollback steps.

## Production guardrails
- Every automated change must include:
  - Before/after behavior summary.
  - Test evidence.
  - Rollback strategy.
- High-risk refactors require manual approval.
- Keep migration in small PR batches (e.g., max 300 lines changed per PR).

## API design (MVP)
- `POST /projects` — create migration project.
- `POST /projects/{id}/ingest` — ingest repository.
- `POST /projects/{id}/plan` — generate migration strategy.
- `POST /projects/{id}/execute` — run selected migration tasks.
- `GET /projects/{id}/report` — retrieve results and quality metrics.
