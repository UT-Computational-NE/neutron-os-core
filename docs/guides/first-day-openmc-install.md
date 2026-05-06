# First-day setup — NeutronOS + OpenMC

Welcome. This guide walks you from a clean Mac/Linux laptop to a working OpenMC + NeutronOS install in about 10 minutes. By the end you'll have:

- OpenMC's traditional Python API + CLI working exactly as the OpenMC documentation describes
- NeutronOS installed, with axiom-ext-openmc bundled — letting you optionally drive OpenMC runs through `neut model run` for live dashboards + signed receipts

**Two commands do all the work.** No hand-editing of configs, no environment puzzles.

---

## Prerequisites

A laptop running macOS or Linux, with:

- A working **conda** install (Miniconda or Anaconda — either is fine)
- A working **Python 3.11+** (conda will provide this in step 1)

If you don't have conda yet: install Miniconda from https://docs.conda.io/en/latest/miniconda.html (5-min, one installer). Windows works via WSL2; if you're on Windows, set up WSL2 first.

---

## Step 1 — Create a class environment + install OpenMC

```bash
conda create -n ne101 python=3.12 -y
conda activate ne101
conda install -c conda-forge openmc -y
```

Verification:

```bash
openmc --version           # CLI
python -c "import openmc"  # Python API (silent on success)
```

If both work, OpenMC is installed and traditional use (write input deck → run `openmc`) is available the way the OpenMC docs describe. If you only ever use OpenMC traditionally, you don't need step 2.

---

## Step 2 — Install NeutronOS

```bash
pip install neutron-os
```

This pulls NeutronOS + the Axiom platform underneath + the `axiom-ext-openmc` adapter that wires OpenMC into NeutronOS for federated dispatch and live observability.

Verification:

```bash
neut --version
neut model --help        # confirms NeutronOS CLI works
axi --version            # confirms Axiom platform is installed
```

---

## Step 3 — Verify both surfaces

### 3a. Traditional OpenMC — unchanged

Write a tiny pin-cell input deck or use one from class materials, then:

```bash
openmc -i geometry.xml
```

This works exactly like vanilla OpenMC. NeutronOS's wrapper does not shadow OpenMC — your traditional workflow is unaffected.

### 3b. NeutronOS-routed OpenMC — bonus path

Same input deck; route through NeutronOS:

```bash
neut model run pin-cell --on local:openmc --tail
```

This:
- Dispatches the run through Axiom's compute primitive
- Shows a **live convergence dashboard** in your terminal
- Signs the result with a per-node Ed25519 keypair
- Composes the receipt into your local memory substrate (so `neut model show pin-cell` later returns the signed result)

If you're new to NeutronOS, this is the "wow" feature — same physics, much richer observability + provenance.

---

## What if step 1 fails?

- **`conda command not found`** — Miniconda isn't on your PATH. Restart your terminal after Miniconda's installer finishes, or `source ~/miniconda3/etc/profile.d/conda.sh`.
- **`Solving environment: failed`** — your conda is stuck on an old solver. Run `conda install -n base conda-libmamba-solver -y && conda config --set solver libmamba`, then retry the `conda install -c conda-forge openmc` line.
- **`openmc: command not found` after install** — the `ne101` env wasn't activated. Run `conda activate ne101` and try again.

---

## What if step 2 fails?

- **`pip: package not found`** — your terminal is using the wrong Python. Confirm with `which python` — should be inside the `ne101` env. If not, `conda activate ne101`.
- **`Could not resolve axiom-ext-openmc`** — version mismatch between NeutronOS and its dependencies. Run `pip install --upgrade neutron-os`.
- **`axi: command not found`** but `neut --version` works — the Axiom CLI may not have been linked to PATH. `axi --help` should still work via `python -m axiom`. Restart the terminal.

---

## What you've built

After step 3 succeeds you have:

- **Native OpenMC** for daily use, exactly as the OpenMC documentation describes — no behavior change
- **NeutronOS as a host nervous system** that can drive the same OpenMC binary with federation, provenance, live observability, and signed artifacts — when you want them
- **Hand-off between the two** is invisible. Use OpenMC traditionally; switch to `neut model run` whenever the bonus surface helps. Same install, same input deck, same answer.

Welcome to the course.
