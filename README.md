# Agentic Migration Factory on GCP

Production-ready starter project for building an **AI Agentic Migration Factory** in GCP.

## What is included

- FastAPI backend that orchestrates migration agents (`discovery`, `planning`, `refactor`, `validation`).
- REST API to create and inspect migration runs.
- Configurable persistence backend:
  - `memory` (default, for local development)
  - `sqlite` (for durable single-instance deployments)
- Request tracing with `X-Request-ID` header and server logs.
- Tests with `pytest`.
- Docker container for Cloud Run deployment.
- Cloud Build pipeline for CI + deployment.
- Terraform infrastructure for GCP setup.
- Helper scripts for one-command dependency install and deployment.
- Step-by-step implementation guide in `docs/06-step-by-step-gcp-implementation.md`.

## Repository structure

- `app/` – API service and migration pipeline.
- `tests/` – API and storage tests.
- `infra/terraform/` – IaC for GCP resources.
- `scripts/install_deps.sh` – local dependency bootstrap.
- `scripts/deploy_gcp.sh` – end-to-end GCP deployment helper.
- `cloudbuild.yaml` – Build/test/deploy pipeline.
- `docs/` – architecture, plan, demo, and end-to-end setup guide.

## Install required dependencies (local)

```bash
./scripts/install_deps.sh
source .venv/bin/activate
```

> If your network blocks PyPI, set `PIP_INDEX_URL` to your internal mirror before running the script.

## Run locally

```bash
# Optional durable local storage
export AMF_STORE_BACKEND=sqlite
export AMF_SQLITE_PATH=./amf.db

pytest
uvicorn app.main:app --reload --port 8080
```

Then open:
- `GET http://localhost:8080/health`
- `POST http://localhost:8080/migrations`

## Deploy to GCP (fully self-serve)

> ⚠️ Before deployment, make sure your GitHub repository contains the full project files.
> If GitHub only shows `.gitkeep`, deployment will fail because `scripts/install_deps.sh`
> and `scripts/deploy_gcp.sh` are missing in that clone.

### Option A: helper script (recommended)

```bash
export PROJECT_ID="<your-project-id>"
export REGION="us-central1"
export SERVICE="agentic-migration-factory"
./scripts/deploy_gcp.sh
```

### Option B: manual

Follow: `docs/06-step-by-step-gcp-implementation.md`

## Troubleshooting: GitHub repo only shows `.gitkeep`

If your GitHub page shows only `.gitkeep` and one commit (for example `Initialize repository`),
publish the full local project first, then clone again.

```bash
# Run this from the local folder that has app/, infra/, scripts/, docs/, etc.
git remote set-url origin https://github.com/<your-user>/Agentic-Migration-Factory.git
git add .
git commit -m "Add complete Agentic Migration Factory project" || true
git push -u origin main

# Verify remote content by cloning fresh
cd ..
rm -rf Agentic-Migration-Factory
git clone https://github.com/<your-user>/Agentic-Migration-Factory.git
cd Agentic-Migration-Factory
ls
```

After this, you should see folders like `app`, `infra`, `scripts`, and `docs`.

## Environment variables

See `.env.example` for all `AMF_*` runtime options.
