# Documentation Tools

**Author:** Ben | **Updated:** 2026-01-22

## Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `md_to_docx.py` | Markdown → Word with diagrams & hyperlinks | `python md_to_docx.py input.md output.docx` |
| `generate_all_docs.py` | Batch generate all docs | `python generate_all_docs.py [--category specs]` |
| `pdf_to_text.py` | Extract text + comments from PDFs | `python pdf_to_text.py doc.pdf -o output.md` |

## Quick Start

```bash
# Generate all documentation
cd /path/to/Neutron_OS/docs/_tools
python generate_all_docs.py

# Single file conversion
python md_to_docx.py ../specs/neutron-os-master-tech-spec.md output.docx
```

## Features

- **Mermaid diagrams** rendered via mermaid.ink API with caching
- **Internal hyperlinks** with bookmarks (Cmd/Ctrl+Click to navigate)
- **Professional formatting** (tables, code blocks, blockquotes)
- **Automatic scaling** for diagrams exceeding page width

## Output

Generated `.docx` files go to `generated/` subdirectory, organized by category.

## Notes

- Clear `.diagram_cache.json` to force diagram regeneration
- Run from source file's directory for correct relative link resolution
- Archived tools and one-offs are in `../_archive/`
