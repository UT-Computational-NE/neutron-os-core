# Rascal Upgrade Playbook

## Prerequisites
- VPN connected to UT Austin network
- SSH access to Rascal (bbooth@rascal.austin.utexas.edu)
- Both repos on the branch/tag you want to deploy

## Quick Upgrade (automated)
```bash
./scripts/upgrade-rascal.sh
```

## Manual Upgrade (if script fails)

### 1. Connect
```bash
ssh bbooth@rascal.austin.utexas.edu
```

### 2. Upgrade Axiom
```bash
cd ~/axiom
git pull  # or rsync from local
pip install -e ".[all]"
```

### 3. Upgrade NeutronOS
```bash
cd ~/Neutron_OS
git pull  # or rsync from local
pip install -e ".[all]"
```

### 4. Verify
```bash
axi mo health --json
neut model materials --card UZrH-20
neut facility list
```

### 5. Re-register agents
```bash
axi agents register
axi agents status
```

## Post-Upgrade Verification
- [ ] `axi mo health` returns healthy
- [ ] `neut model materials` shows 11 materials
- [ ] `neut facility list` shows 3 packs
- [ ] `axi agents status` shows Mo, D-FIB, PR-T running
- [ ] K3D pods healthy: `kubectl get pods -A`

## Troubleshooting
- **"Module not found"**: Run `pip install -e ".[all]"` again
- **K3D pods down**: `k3d cluster start axiom-dev`
- **Mo not running**: `axi agents register && axi agents start mo`

## Index NETL Docs (Release 2 prep)
```bash
axi rag index /path/to/netl-docs/
axi rag status
axi rag search "control rod calibration"  # spot check
```
