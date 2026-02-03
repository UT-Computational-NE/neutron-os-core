# Neutron OS - Project Memory

## Documentation Strategy

### How to Avoid Duplication

**Each document owns ONE vertical:**
- **CONTRIBUTING.md** — Git workflow, branching, .gitignore maintenance
- **CLAUDE.md** (this file) — Terminology, tech choices, project memory
- **docs/README.md** — Documentation folder structure (ADR/PRD/specs)
- **PUBLISHER_USAGE.md** — OneDrive publishing workflow

**Golden Rule:** Link, don't duplicate. If you're repeating information, move it to the appropriate doc and link from others.

**Example:** Don't repeat terminology in CONTRIBUTING.md. Instead, write "See CLAUDE.md terminology standards" with a link.

### When to Update Documentation

1. **Add a new tool/language?** → Update .gitignore + add pattern reference to CONTRIBUTING.md
2. **New architectural decision?** → Create ADR in docs/adr/ + link from docs/README.md
3. **New terminology or naming convention?** → Add to CLAUDE.md → link from CONTRIBUTING.md if relevant
4. **New publishing workflow?** → Update PUBLISHER_USAGE.md → link from CONTRIBUTING.md

---

## Git & Repository Standards

### .gitignore Philosophy
- **Automate exclusions** for all generated/environment files
- **Never commit** build artifacts, dependencies, secrets, or data files
- **Update .gitignore** when adding new tools/languages (separate commit)
- Base patterns on [GitHub's Python template](https://github.com/github/gitignore/blob/main/Python.gitignore)
- See [CONTRIBUTING.md](CONTRIBUTING.md) for maintenance workflow

### Why This Matters
Large binary files, data, and build artifacts bloat git history and slow cloning. Consistent .gitignore standards across all 6 digital twin projects ensure:
- Clean repository history
- Fast clone/pull operations  
- No accidental secrets in commits
- Consistent developer experience

## Documentation Conventions

### Generated Files
- **Word docs (.docx)** go to `docs/_tools/generated/` subdirectories, NOT alongside source markdown
- Structure mirrors source: `docs/specs/*.md` → `docs/_tools/generated/specs/*.docx`
- Pandoc command for tech spec:
  ```bash
  cd docs/specs
  pandoc neutron-os-master-tech-spec.md -o ../\_tools/generated/specs/neutron-os-master-tech-spec.docx --toc --toc-depth=3
  ```

### Mermaid Diagrams (for Word export)
- **NEVER use ASCII diagrams** - always use Mermaid diagrams for better rendering
- ASCII art boxes (┌─┐│└┘) should be converted to Mermaid format
- Subgraph titles: **<16 characters** to prevent text clipping
- Use `TB` (top-to-bottom) flow for portrait-oriented Word docs
- No `**bold**` or bullet lists inside diagram nodes
- Color contrast: `#000000` on light fills, `#ffffff` on dark fills

## Terminology Standards

| Use This | Not This |
|----------|----------|
| Provider | Plugin |
| Factory | (internal pattern for Provider instantiation) |
| Extension Point | Plugin hook |
| Priority Module | Active Module |
| Future Module | Planned Module |
| DataTransformer | Transformer |

## INL Partnership Framing
- Position Neutron OS and DeepLynx as **independent peer platforms**
- Avoid implying Neutron OS is subordinate or "built atop" DeepLynx
- Use hypothetical language ("proposed", "potential", "would") for partnership details

## Tech Stack (Local Dev)
- K3D for local Kubernetes
- PostgreSQL for all environments (no SQLite)
- Terraform for AWS/Azure/GCP
