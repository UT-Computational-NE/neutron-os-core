#!/usr/bin/env bash
set -euo pipefail

# Rascal Upgrade Script
# Usage: ./scripts/upgrade-rascal.sh [user@host]

RASCAL="${1:-bbooth@rascal.austin.utexas.edu}"
AXIOM_SRC="/Users/ben/Projects/UT_Computational_NE/axiom"
NEUTOS_SRC="/Users/ben/Projects/UT_Computational_NE/Neutron_OS"

echo "=== Upgrading Rascal: $RASCAL ==="
echo ""

# Step 1: Check connectivity
echo "[1/7] Checking SSH connectivity..."
ssh -o ConnectTimeout=5 "$RASCAL" "echo 'Connected'" || {
    echo "ERROR: Cannot reach $RASCAL. Is VPN connected?"
    exit 1
}

# Step 2: Sync Axiom source
echo "[2/7] Syncing Axiom source..."
rsync -az --delete \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.pytest_cache' \
    --exclude 'node_modules' \
    --exclude '.venv' \
    "$AXIOM_SRC/" "$RASCAL:~/axiom/"

# Step 3: Sync NeutronOS source
echo "[3/7] Syncing NeutronOS source..."
rsync -az --delete \
    --exclude '.git' \
    --exclude '__pycache__' \
    --exclude '*.pyc' \
    --exclude '.pytest_cache' \
    --exclude 'node_modules' \
    --exclude '.venv' \
    "$NEUTOS_SRC/" "$RASCAL:~/Neutron_OS/"

# Step 4: Install on Rascal
echo "[4/7] Installing Axiom..."
ssh "$RASCAL" 'cd ~/axiom && pip install -e ".[all]" -q'

echo "[5/7] Installing NeutronOS..."
ssh "$RASCAL" 'cd ~/Neutron_OS && pip install -e ".[all]" -q'

# Step 6: Run post-install checks
echo "[6/7] Running post-install verification..."
ssh "$RASCAL" 'axi --version && neut --help > /dev/null && echo "CLI: OK"'
ssh "$RASCAL" 'axi mo health --json 2>/dev/null | python3 -c "import sys,json; d=json.load(sys.stdin); print(f\"Health: {d.get(\"status\", \"unknown\")}\")" || echo "Health: check manually"'
ssh "$RASCAL" 'neut model materials --card UZrH-20 > /dev/null && echo "Model Corral: OK" || echo "Model Corral: FAILED"'
ssh "$RASCAL" 'neut facility list > /dev/null && echo "Facility Packs: OK" || echo "Facility Packs: FAILED"'

# Step 7: Register agent services
echo "[7/7] Re-registering agent services..."
ssh "$RASCAL" 'axi agents register 2>/dev/null || echo "Agent registration: check manually"'

echo ""
echo "=== Upgrade complete ==="
echo "Run 'axi nodes status rascal' to verify from your local machine."
