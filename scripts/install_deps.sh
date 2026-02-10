#!/usr/bin/env bash
set -euo pipefail

# Resolve Python launcher across Linux/macOS and Windows Git Bash.
if command -v python >/dev/null 2>&1; then
  PYTHON_CMD=(python)
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=(py -3)
else
  echo "ERROR: Python not found. Install Python 3.10+ and ensure 'python' or 'py' is on PATH."
  echo "On Windows, disable the Microsoft Store app alias if it hijacks 'python'."
  exit 1
fi

"${PYTHON_CMD[@]}" -m venv .venv

# Use venv-local python directly for reliability.
if [[ -x .venv/bin/python ]]; then
  VENV_PYTHON=.venv/bin/python
elif [[ -x .venv/Scripts/python.exe ]]; then
  VENV_PYTHON=.venv/Scripts/python.exe
elif [[ -x .venv/Scripts/python ]]; then
  VENV_PYTHON=.venv/Scripts/python
else
  echo "ERROR: Virtual environment created but Python executable was not found."
  exit 1
fi

"$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel

# Optional: provide internal mirror if direct pypi is blocked.
# Example: export PIP_INDEX_URL=https://<your-mirror>/simple
if [[ -n "${PIP_INDEX_URL:-}" ]]; then
  echo "Using custom PIP_INDEX_URL=$PIP_INDEX_URL"
fi

"$VENV_PYTHON" -m pip install -r requirements.txt
"$VENV_PYTHON" -m pip check

if [[ -f .venv/bin/activate ]]; then
  echo "Dependencies installed. Activate with: source .venv/bin/activate"
elif [[ -f .venv/Scripts/activate ]]; then
  echo "Dependencies installed. Activate with: source .venv/Scripts/activate"
fi
