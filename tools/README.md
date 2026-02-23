Tools Directory — Policy and Intent

Purpose
- `tools/` is the canonical home for reusable scripts and runtime Python packages that are consumed by automation and CI.

Guidelines
- Place production-ready Python packages under `tools/<package_name>/`.
- Avoid duplicate copies of the same package elsewhere in the repo. If a legacy copy exists, archive or remove it and prefer the `tools/` location.
- If a package must remain available at the repo root for compatibility, provide a small shim that re-exports the canonical package (see `cost_estimation_tool/__init__.py`).

CI and Automation
- CI should import packages from `tools/` when running tests or publishing packages.
- Add checks to CI that detect duplicate package names across the repository and fail the build with instructions to consolidate.

Contact
- Ownership: Add the package owner(s) to `CODEOWNERS` to avoid accidental duplication.
