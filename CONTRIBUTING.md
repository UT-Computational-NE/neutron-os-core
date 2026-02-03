# Contributing to Neutron OS

**Sections:**
- [Development Setup](#development-setup)
- [Git Workflow](#git-workflow)
- [Code Conventions](#code-conventions)
- [Documentation](#documentation)
- [Standards & References](#standards--references)

## Development Setup

```bash
git clone https://rsicc-gitlab.tacc.utexas.edu/neutron-os/neutron-os-core.git
cd neutron_os
# Your IDE will auto-detect .gitignore patterns
```

**Local Testing**
```bash
# Validate .gitignore patterns before committing
git check-ignore -v your_file_pattern

# Run full test suite before pushing
bazel test //...
```

## Git Workflow

### Committing Code
1. Create a feature branch: `git checkout -b feature/description`
2. Make changes and commit with clear messages
3. Push and open a merge request

### What Gets Ignored

Our `.gitignore` automatically excludes:
- **Python artifacts**: `__pycache__`, `.venv`, `.pytest_cache`, `*.egg-info`
- **Environment files**: `.env`, `.env.local` (never commit secrets!)
- **Build outputs**: `build/`, `dist/`, `*.so`
- **IDE files**: `.vscode/`, `.idea/`, `*.swp`
- **Data/Logs**: `*.csv`, `*.h5`, `*.log`, `logs/`
- **Generated docs**: `docs/_tools/generated/`, `docs/_tools/test/`

**No action needed** — these patterns apply automatically when you clone the repo.

### Maintaining .gitignore

When adding a new tool, language, or dependency type:

1. **Check for existing patterns** in `.gitignore` first
2. **Add patterns following existing style** (grouped by category with comments)
3. **Test locally**: 
   ```bash
   git check-ignore -v your_file_pattern
   ```
4. **Commit as separate change**:
   ```bash
   git add .gitignore
   git commit -m "Update .gitignore: add [tool/language] patterns"
   ```
5. **Open merge request** for visibility to team

### Pattern Examples

```bash
# OS artifacts
.DS_Store
.AppleDouble

# Python: bytecode and packages
__pycache__/
*.py[cod]
*.egg-info/

# Data: don't commit large files
*.parquet
*.h5

# Environment: NEVER commit secrets
.env
.env.local
```

**Golden Rule:** If it's a file you don't want 100 copies of in git history, add it to `.gitignore`.

## Code Conventions

For naming, terminology, and architectural patterns, see [CLAUDE.md](CLAUDE.md).

**Examples:**
- Use `DataTransformer` not `Transformer` (see terminology standards in CLAUDE.md)
- Use `Provider` not `Plugin` for extension system
- PostgreSQL everywhere, no SQLite (see CLAUDE.md tech stack section)

## Documentation

### Writing Documentation

See [docs/README.md](docs/README.md) for folder structure and conventions:
- **ADR/** — Architecture Decision Records (technical decisions, immutable)
- **PRD/** — Product Requirements (what we're building, user journeys)
- **specs/** — Technical Specifications (how to build it)

### Publishing Documentation

When your docs are ready, see [PUBLISHER_USAGE.md](PUBLISHER_USAGE.md) for publishing to OneDrive.

First-time publishers? Start with [PUBLISH_CHECKLIST.md](PUBLISH_CHECKLIST.md) to set up Azure credentials (one-time setup).

### Generated Outputs

- Generated Word docs go to `docs/_tools/generated/` (not alongside source markdown)
- Mermaid diagrams for Word export: see `CLAUDE.md` → Mermaid Diagrams section

## Standards & References

**Project Standards:**
- [CLAUDE.md](CLAUDE.md) — Terminology, tech stack, project memory
- [docs/README.md](docs/README.md) — Documentation structure & conventions

**External References:**
- [GitHub Python .gitignore](https://github.com/github/gitignore/blob/main/Python.gitignore) — Base patterns
- [Bazel Documentation](https://bazel.build/docs) — Build system reference
