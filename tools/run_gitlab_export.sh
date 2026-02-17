#!/bin/bash
# Weekly GitLab export runner for launchd
# Outputs to exports/ directory in this folder

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
EXPORT_DIR="${SCRIPT_DIR}/exports"
VENV_PYTHON="/Users/ben/Projects/UT_Computational_NE/.venv/bin/python"
LOG_FILE="${EXPORT_DIR}/export.log"

# Create exports directory if needed
mkdir -p "$EXPORT_DIR"

# Source token from secure location (keychain or env file)
# Option 1: From a .env file (not committed)
if [[ -f "${SCRIPT_DIR}/.env" ]]; then
    source "${SCRIPT_DIR}/.env"
fi

# Option 2: From macOS Keychain (more secure)
# Uncomment and use this instead of .env:
# export GITLAB_TOKEN=$(security find-generic-password -s "gitlab-tracker-token" -w 2>/dev/null)

# Verify token is set
if [[ -z "$GITLAB_TOKEN" ]]; then
    echo "$(date): ERROR - GITLAB_TOKEN not set" >> "$LOG_FILE"
    exit 1
fi

# Run the export
echo "$(date): Starting GitLab export..." >> "$LOG_FILE"
cd "$SCRIPT_DIR"
"$VENV_PYTHON" gitlab_tracker_export.py --output-dir "$EXPORT_DIR" >> "$LOG_FILE" 2>&1

echo "$(date): Export complete" >> "$LOG_FILE"

# Keep only the last 8 exports (2 months of weekly)
cd "$EXPORT_DIR"
ls -t gitlab_export_*.json 2>/dev/null | tail -n +9 | xargs -r rm -f
