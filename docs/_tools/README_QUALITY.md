# Documentation Quality Tools

## Overview

This directory contains automated tools for maintaining high-quality documentation, particularly focusing on Mermaid diagram consistency and visual quality.

## Main Tool: `doc_quality_checker.py`

A comprehensive documentation quality checker that can both detect and fix common issues in Mermaid diagrams.

### Features

- **Color Contrast Checking**: Ensures proper text color on backgrounds
  - Light backgrounds get dark text (#000000)
  - Dark backgrounds get light text (#ffffff)
  - Detects missing color properties
  
- **Arrow Styling**: Enforces consistent arrow appearance
  - Standard color: #777777
  - Standard width: 3px
  - Adds missing linkStyle declarations
  
- **Subgraph Title Length**: Warns about titles over 35 characters that may wrap

- **Repeatable**: Can be run multiple times safely - only fixes actual issues

### Usage

#### Check for issues (no changes):
```bash
python3 doc_quality_checker.py
```

#### Check with verbose output:
```bash
python3 doc_quality_checker.py --verbose
```

#### Automatically fix issues:
```bash
python3 doc_quality_checker.py --fix
```

#### Check specific issue type:
```bash
python3 doc_quality_checker.py --type missing_color
```

### Issue Types

- `missing_color`: Style statements without explicit text color
- `light_on_light`: Light text on light background (poor contrast)
- `dark_on_dark`: Dark text on dark background (poor contrast)
- `missing_linkstyle`: Diagrams with connections but no arrow styling
- `wrong_arrow_color`: Arrows not using standard #777777 color
- `wrong_stroke_width`: Arrows not using standard 3px width
- `long_subgraph_title`: Subgraph titles over 35 characters

## Helper Scripts

### `check_and_fix_docs.sh`
Interactive script for checking and optionally fixing issues, then regenerating documents.

```bash
./check_and_fix_docs.sh
```

### `doc_quality_ci.py`
CI/CD-friendly quality gate that returns non-zero exit code if issues are found.

```bash
python3 doc_quality_ci.py
```

## Integration with Document Generation

The quality checker should be run before generating Word documents to ensure:
1. All diagrams have proper color contrast
2. Arrow styling is consistent
3. Diagrams will render correctly in Word

### Recommended Workflow

1. **During Development**: Run checker after editing markdown files
   ```bash
   python3 doc_quality_checker.py --fix
   ```

2. **Before Committing**: Ensure no issues remain
   ```bash
   python3 doc_quality_ci.py
   ```

3. **Generate Documents**: After fixes are applied
   ```bash
   python3 generate_all_docs.py
   ```

## Color Standards

### Light Backgrounds (need dark text)
- Material Design light colors: #e3f2fd, #e8f5e9, #f3e5f5, etc.
- Light orange: #fff3e0
- Light red: #ffcdd2
- White: #ffffff, #fff

### Dark Backgrounds (need light text)  
- Material Design dark colors: #1976d2, #388e3c, #7b1fa2, etc.
- Dark grey: #263238, #424242, #455a64
- Dark brown: #5d4037, #3e2723

### Standard Elements
- Arrow color: #777777
- Arrow width: 3px
- Default text on light: #000000
- Default text on dark: #ffffff

## Exit Codes

The quality checker returns:
- `0`: No issues found or all issues fixed
- `1`: Issues found (useful for CI/CD pipelines)

## Maintenance

The tool is designed to be extended. To add new checks:

1. Add a new `IssueType` enum value
2. Implement the check in `check_diagram()` or related method
3. Add fix logic in `fix_issues()` if auto-fixable

## Legacy Scripts (Deprecated)

The following scripts have been consolidated into `doc_quality_checker.py`:
- `fix_mermaid_colors.py` - Now handled by color checking features
- `fix_subgraph_titles.py` - Now handled by title length checking
- `find_missing_colors.py` - Now handled by missing color detection

These can be safely removed after verifying the new tool works correctly.