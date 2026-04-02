# Neutron OS

**Nuclear Energy Unified Technology for Research, Operations & Networks**

A modular digital platform for nuclear facilities that unifies data management, operations tracking, experiment scheduling, and analytics — replacing fragmented workflows (paper logs, spreadsheets, phone calls) with integrated digital tools.

## Key Capabilities

- **Model Corral** — Physics model registry with 18 commands: init, validate, add, clone, search, list, show, pull, lineage, diff, export, audit, generate, lint, sweep, materials, share, receive — plus review, reviews, resolve, invite, contributors, status
- **Materials** — 11 verified compositions with MCNP/MPACT card generation
- **Facility Packs** — NETL-TRIGA, MSRE, PWR-generic with 8 commands: list, show, install, uninstall, init, publish, materials, sync
- **CoreForge Bridge** — Integration with CoreForge neutronics tools
- **Federation Model Sharing** — Share and receive models across federated nodes
- **Signal Pipeline** — Ingest signals from voice memos, Teams, GitLab, Linear, and freetext; extract structured insights; publish weekly briefings
- **Publisher** — Document lifecycle management with provider-based generation, storage, and review
- **Interactive Agent** — Chat-based assistant with facility context (`neut chat`)
- **Self-Diagnostics** — AI-powered troubleshooting (`neut doctor`)
- **Extension System** — Scaffold and manage facility-specific extensions (`neut ext`)
- **MCP Server** — IDE integration via Model Context Protocol (`neut serve-mcp`)

## Quick Start

```bash
pip install neutron-os

# Or from source
git clone https://rsicc-gitlab.tacc.utexas.edu/ut-computational-ne/neutron-os-core.git
cd neutron-os-core
pip install -e ".[all]"

# Or use the bootstrap script (creates venv, installs, sets up direnv)
./scripts/bootstrap.sh

# Verify
neut --help
neut doctor

# Run the onboarding demo
neut demo run collaborator
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed setup instructions including direnv, venv, and troubleshooting.

## Repository Structure

```
Neutron_OS/
├── src/neutron_os/       # Python package root
│   ├── neut_cli.py       #   CLI entry point
│   ├── infra/            #   Shared infra (gateway, orchestrator, auth)
│   └── extensions/       #   Extension system
│       └── builtins/     #     Builtin extensions (sense, docflow, chat, demo…)
├── runtime/              # Instance data (config, inbox, sessions — gitignored)
├── tests/                # Cross-cutting tests
├── docs/                 # Architecture specs, PRDs, design docs
├── infra/                # Terraform, Helm, K3D configs
├── scripts/              # Bootstrap and installation scripts
├── pyproject.toml        # Package definition (Hatchling)
├── Makefile              # Dev commands (test, build, lint, clean)
└── CLAUDE.md             # AI assistant context and project conventions
```

## CLI

```bash
# Model Corral (18+ commands)
neut model add ./input.i               # Auto-detect and register a model
neut model list                         # Browse registered models
neut model search --code mcnp           # Search by code type
neut model validate ./input.i           # Validate model file
neut model materials                    # List available materials
neut model generate --material UO2      # Generate MCNP/MPACT cards
neut model review <id>                  # Start a collaborative review
neut model share <id>                   # Share via federation

# Facility Packs (8 commands)
neut facility list                      # Available packs
neut facility install NETL-TRIGA        # Install a facility pack
neut facility sync                      # Sync with upstream

# Platform
neut chat                              # Interactive agent
neut signal pipeline ingest             # Run signal ingestion
neut pub publish                       # Generate and publish documents
neut doctor                            # AI-powered diagnostics
neut ext init my-extension             # Create a new extension
neut demo run collaborator             # Guided onboarding walkthrough
```

## Development

```bash
make test              # 415+ tests
make integration       # Integration tests (needs .env credentials)
make lint              # Ruff linter
make build             # Build wheel
make clean             # Remove build artifacts
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| CLI & Agents | Python (argparse, rich, prompt-toolkit) |
| LLM Gateway | Model-agnostic (Anthropic, OpenAI, any OpenAI-compatible) |
| Data Platform | Apache Iceberg + DuckDB + Dagster + dbt |
| Database | PostgreSQL + pgvector |
| Infrastructure | Terraform, Helm, K3D |
| CI/CD | GitLab CI with AI code review |
| Packaging | Hatchling (pip-installable wheel) |

## Design Principles

- **Reactor-agnostic core** with facility-specific config
- **Offline-first** — queue locally, sync on restore
- **Human-in-the-loop** for all writes in safety-adjacent contexts
- **No vendor lock-in** — model-agnostic, cloud-agnostic, IDE-agnostic
- **Provider pattern** — swap implementations via config, not code changes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development workflow, git practices, and conventions.

## License

MIT
