# 06 — Complete Step-by-Step Build Procedure (GCP)

This guide explains **what to do at each step** and **why that step exists**.

## Prerequisites (you must have these before starting)

- A GCP project with billing enabled
- `gcloud` CLI installed and authenticated (`gcloud auth login`)
- Terraform >= 1.5
- Docker installed locally
- Python 3.10+

Project inputs you must decide:
- `PROJECT_ID`
- `REGION`
- public vs authenticated-only API access

You can run everything with the helper script (`scripts/deploy_gcp.sh`) or manually with the steps below.

---


## Common blocker: GitHub repo has only `.gitkeep`

If your GitHub repository page shows only `.gitkeep` and an initial commit, you cloned an empty remote.
In that case, `./scripts/install_deps.sh` and `./scripts/deploy_gcp.sh` will fail with “No such file or directory”.

### Fix
1. Push the full project content (`app/`, `infra/`, `scripts/`, `docs/`, `requirements.txt`, etc.) to `main`.
2. Clone fresh and confirm those folders exist before running deployment commands.

```bash
# from the machine/folder that already has the full project files
git remote set-url origin https://github.com/<your-user>/Agentic-Migration-Factory.git
git add .
git commit -m "Add complete Agentic Migration Factory project" || true
git push -u origin main

# then re-clone and verify
cd ..
rm -rf Agentic-Migration-Factory
git clone https://github.com/<your-user>/Agentic-Migration-Factory.git
cd Agentic-Migration-Factory
ls
```

## Step 1: Create and configure your GCP project

### What you do
1. Create a new project (or select one).
2. Set gcloud defaults.

```bash
gcloud config set project <PROJECT_ID>
gcloud config set run/region us-central1
```

### Why
All later resources (Cloud Run, Artifact Registry, Cloud Build) are scoped to one project and region.

---

## Step 2: Provision infrastructure with Terraform

### What you do
1. Move to Terraform folder.
2. Initialize providers.
3. Plan and apply.

```bash
cd infra/terraform
terraform init
terraform plan -var="project_id=<PROJECT_ID>"
terraform apply -var="project_id=<PROJECT_ID>"
```

### Why
Terraform creates repeatable production infrastructure:
- API enablement (`run`, `artifactregistry`, `cloudbuild`, `secretmanager`)
- Docker repository for images
- Runtime service account
- Cloud Run service template
- Public invoker IAM binding

---

## Step 3: Install app requirements and validate locally

### What you do

```bash
python -m venv .venv
source .venv/bin/activate   # Windows Git Bash: source .venv/Scripts/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Why
You verify agent orchestration and API correctness before cloud deployment.

### Smoke test examples

```bash
curl http://localhost:8080/health
curl -X POST http://localhost:8080/migrations \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/example/legacy-monolith",
    "language": "python",
    "target_architecture": "cloud-run-microservices"
  }'
```

---

## Step 4: Build and push the container

### What you do

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev

docker build -t us-central1-docker.pkg.dev/<PROJECT_ID>/agentic-migration-factory/api:latest .
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/agentic-migration-factory/api:latest
```

### Why
Cloud Run deploys from container images stored in Artifact Registry.

---

## Step 5: Deploy via Cloud Build pipeline

### What you do

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions _SERVICE=agentic-migration-factory,_REGION=us-central1,_IMAGE=us-central1-docker.pkg.dev/<PROJECT_ID>/agentic-migration-factory/api:$(git rev-parse --short HEAD)
```

### Why
Cloud Build enforces production flow:
1. Install dependencies
2. Run tests
3. Build image
4. Push image
5. Deploy Cloud Run revision

---

## Step 6: Verify deployed API

### What you do
1. Read service URL from Terraform output or Cloud Run console.
2. Execute health + migration calls.

```bash
curl https://<CLOUD_RUN_URL>/health
curl -X POST https://<CLOUD_RUN_URL>/migrations \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/example/legacy-monolith",
    "language": "python",
    "target_architecture": "cloud-run-microservices"
  }'
```

### Why
Confirms API is reachable and full agentic workflow works in managed infrastructure.

---

## Step 7: Operate in production

### What you do
- Use Cloud Logging for request tracing.
- Configure Error Reporting alerts.
- Set minimum instances in Cloud Run for lower cold-start latency.
- Lock IAM to authenticated invokers if public access is not required.

### Why
Production readiness requires observability, access control, and predictable runtime behavior.

---

## Step 8: Extend to full migration factory

### What you do next
- Replace in-memory store with Firestore or Cloud SQL.
- Add Pub/Sub + Cloud Tasks for asynchronous long-running migrations.
- Connect to Vertex AI for LLM-generated code transformations.
- Add GitHub/GitLab app integration to open real migration PRs automatically.

### Why
This repo is the production foundation; these upgrades turn it into enterprise-scale autonomous migration operations.


## Fast path (single command deployment)

### What you do

```bash
export PROJECT_ID="<PROJECT_ID>"
export REGION="us-central1"
export SERVICE="agentic-migration-factory"
./scripts/deploy_gcp.sh
```

### Why
The script executes Terraform apply + Cloud Build deployment in order, and prints the Cloud Run URL at the end.
