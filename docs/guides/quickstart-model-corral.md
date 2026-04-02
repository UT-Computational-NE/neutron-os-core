# Model Corral Quick Start

## Install

```bash
pip install neutron-os
neut setup
```

## Your First Model (5 minutes)

### 1. Create a model
```bash
neut model init my-triga-model --reactor-type TRIGA --materials
cd my-triga-model/
```
This creates `model.yaml` with NETL-TRIGA materials pre-populated.

### 2. Add your input files
Copy your MCNP input deck into the directory, then edit `model.yaml`:
- Fill in `description`
- Update `facility` (e.g., NETL)
- Add tags

### 3. Validate
```bash
neut model validate .
```

### 4. Submit to registry
```bash
neut model add . -m "initial steady-state model"
```

### 5. Search and browse
```bash
neut model list
neut model search triga
neut model show my-triga-model
```

### 6. Pull a model
```bash
neut model pull my-triga-model ./workspace
```

## Materials

Browse verified nuclear material compositions:
```bash
neut model materials                          # list all
neut model materials --category fuel          # filter by category
neut model materials --card UZrH-20           # generate MCNP card
neut model materials --card H2O --format mpact  # MPACT format
```

## Generate MCNP Cards

If your `model.yaml` has a `materials` section:
```bash
neut model generate . --format mcnp           # to stdout
neut model generate . --format mcnp -o mat.i  # to file
```

## Facility Packs

Pre-loaded materials and parameters for known reactors:
```bash
neut facility list                             # see installed packs
neut facility materials NETL-TRIGA            # browse pack materials
neut facility materials NETL-TRIGA --format mcnp  # all materials as MCNP cards
```

## For CoreForge Users (Cole)

Register a CoreForge-generated model with provenance:
```bash
neut model add ./coreforge-output --from-coreforge --coreforge-config config.py
```

The CoreForge version, config file hash, and builder specs are captured automatically.

## Common Workflows

**Edit an existing model:**
```bash
neut model pull netl-steady-state ./workspace
# edit files...
neut model validate ./workspace/netl-steady-state
neut model add ./workspace/netl-steady-state -m "updated control rods"
```

**Fork and modify:**
```bash
neut model clone netl-steady-state --name my-variant
# opens in your editor automatically
```

## Getting Help

```bash
neut model --help                # show available commands
neut model <command> --help      # help for a specific command
neut model materials --help      # material-specific options
```

All commands support `--json` for machine-readable output.
