# Git Integration for md_to_docx.py

## Overview

The `md_to_docx.py` converter now supports Git-aware processing, allowing you to convert only markdown files that have changed since your last commit. This improves workflow efficiency by avoiding unnecessary re-processing of unchanged documents.

## New Feature: `--changed` Flag

### Usage

```bash
python md_to_docx.py <source_dir> <output_dir> --all --changed
```

### How It Works

1. **Detects Changed Files**: Queries Git to find markdown files that are:
   - Modified but unstaged
   - Staged for commit
   - Untracked files

2. **Filters Conversion**: Only processes markdown files within the source directory that have changed

3. **Graceful Fallback**: If the source directory is not in a Git repository, the script returns an empty set and reports "No changed markdown files found in Git"

### Examples

**Convert all changed markdown files in a directory:**
```bash
python md_to_docx.py ./specs ./generated --all --changed
```

**Convert with pregeneration (async diagram rendering) enabled:**
```bash
python md_to_docx.py ./specs ./generated --all --changed --pregenerate
```

**View help for available options:**
```bash
python md_to_docx.py --help
```

## Implementation Details

### New Function: `get_changed_files(src_path: Path) -> set[Path]`

Located at line 131 in `md_to_docx.py`, this function:

- Queries `git diff` for modified/unstaged files
- Queries `git diff --cached` for staged files  
- Queries `git ls-files --others --exclude-standard` for untracked files
- Combines results and filters to markdown files within the source path
- Returns an empty set if not in a Git repository (graceful error handling)

### Modified Function: `convert_all_docs()`

Added `changed_only: bool = False` parameter to support Git filtering:

- When `changed_only=True`, calls `get_changed_files()` to get the set of changed markdown files
- Filters the discovered markdown files to only those that are in the changed set
- Properly handles path resolution (absolute vs relative paths) for accurate matching

### Modified Function: `main()`

Added `--changed` argument to CLI:
- Works only in combination with `--all` flag (batch conversion)
- Passes `changed_only=args.changed` to `convert_all_docs()`
- Documented in help output

## Workflow Example

```bash
# Edit some markdown files
$ vim docs/architecture.md
$ vim docs/api-reference.md

# Check what changed
$ git status
On branch main
Changes not staged for commit:
    modified: docs/architecture.md
    modified: docs/api-reference.md

# Convert ONLY the changed files to Word
$ python docs/_tools/md_to_docx.py ./docs/specs ./docs/generated --all --changed
Found 2 changed markdown file(s)

Converting 2 markdown file(s)...
Output: docs/generated

[1/2] architecture.md
  ✓ Generated: architecture.docx
[2/2] api-reference.md
  ✓ Generated: api-reference.docx

Completed: 2 file(s)
```

## Notes

- The `--changed` flag is optional and defaults to `false`
- When `--changed` is NOT specified, all markdown files are processed (original behavior)
- The script is Git-repository aware - it automatically detects the repository root
- If the directory is not in a Git repository, the feature gracefully disables with a message
- Works seamlessly with all other conversion options (`--draft`, `--pregenerate`, `--skip`)

## Testing

Git integration was tested with:
1. Non-Git directories (graceful fallback to empty set)
2. Git repository with no changes (reports "No changed markdown files found in Git")
3. Git repository with modified files (correctly identifies and processes only changed files)
4. Multiple changed files with selective conversion (only specified files processed)
