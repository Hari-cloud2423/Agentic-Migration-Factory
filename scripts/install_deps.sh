#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools wheel

# Optional: provide internal mirror if direct pypi is blocked.
# Example: export PIP_INDEX_URL=https://<your-mirror>/simple
if [[ -n "${PIP_INDEX_URL:-}" ]]; then
  echo "Using custom PIP_INDEX_URL=$PIP_INDEX_URL"
fi

python -m pip install -r requirements.txt
python -m pip check
