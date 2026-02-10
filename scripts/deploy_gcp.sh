#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-$(gcloud config get-value project 2>/dev/null || true)}"
REGION="${REGION:-us-central1}"
SERVICE="${SERVICE:-agentic-migration-factory}"
IMAGE="${IMAGE:-${REGION}-docker.pkg.dev/${PROJECT_ID}/agentic-migration-factory/api:$(git rev-parse --short HEAD)}"

if [[ -z "$PROJECT_ID" || "$PROJECT_ID" == "(unset)" ]]; then
  echo "ERROR: PROJECT_ID is not set and no default gcloud project found."
  exit 1
fi

echo "Using PROJECT_ID=$PROJECT_ID REGION=$REGION SERVICE=$SERVICE"

gcloud config set project "$PROJECT_ID"
gcloud config set run/region "$REGION"

pushd infra/terraform >/dev/null
terraform init
terraform apply -auto-approve -var="project_id=${PROJECT_ID}" -var="region=${REGION}" -var="service_name=${SERVICE}"
popd >/dev/null

gcloud builds submit --config cloudbuild.yaml \
  --substitutions _SERVICE="$SERVICE",_REGION="$REGION",_IMAGE="$IMAGE"

echo "Deployment submitted. Query URL:"
gcloud run services describe "$SERVICE" --region "$REGION" --format='value(status.url)'
