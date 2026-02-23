Repository Folder Intents

This file documents the intended purpose for key top-level folders so contributors and automation respect repository structure.

- `tools/`: Canonical runtime tools and packages used by automation and CI. Production-ready packages should live here.
- `docs/`: Documentation and doc-generation tools. Generated artifacts go to `docs/_tools/generated/` and are git-ignored.
- `services/`, `packages/`, `plugins/`: Host service implementations and consumer-facing packages.
- `Neutron_OS/`: The platform-specific code and configurations; prefer `tools/` for shared packages.

Enforcement ideas
- CI job: `check-folder-intents` — scans for duplicate package names and for packages living outside `tools/` and warns or fails.
- Pre-commit hook: run a script to detect duplicate module names and notify authors.
- `CODEOWNERS`: Assign owners for folders to make consolidation decisions explicit.
