# Neutron OS - Project Memory

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
