"""CLI handler for `neut model` — physics model registry.

Usage:
    neut model init <name>              Scaffold a new model directory
    neut model validate <path>          Validate a model against schema
    neut model add <path>               Submit model to registry
    neut model search <query>           Search models
    neut model list [--filters]         List models with filters
    neut model show <model_id>          Show model details
    neut model pull <model_id> [dest]   Download model
    neut model lineage <model_id>       Show ROM → physics chain
    neut model diff <id_a> <id_b>       Compare two models
    neut model export <model_id>        Export as ZIP archive
    neut model audit [--since DATE]     View change history
"""

from __future__ import annotations

import argparse
import json
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="neut model",
        description="Physics model registry — versioning, validation, and provenance",
    )
    sub = parser.add_subparsers(dest="action")

    # init
    init_p = sub.add_parser("init", help="Scaffold a new model directory")
    init_p.add_argument("name", help="Model name (kebab-case)")
    init_p.add_argument(
        "--reactor-type", help="Reactor type (TRIGA, MSR, PWR, BWR, HTGR, SFR, custom)"
    )
    init_p.add_argument(
        "--physics-code", help="Physics code (MCNP, VERA, SAM, Griffin, OpenMC, etc.)"
    )
    init_p.add_argument("--facility", help="Facility identifier (e.g., NETL, MIT)")

    # validate
    val_p = sub.add_parser("validate", help="Validate a model directory")
    val_p.add_argument("path", help="Path to model directory")
    val_p.add_argument("--format", choices=["human", "json"], default="human")

    # add
    add_p = sub.add_parser("add", help="Submit model to registry")
    add_p.add_argument("path", help="Path to model directory")
    add_p.add_argument("-m", "--message", default="", help="Submission message")

    # search
    search_p = sub.add_parser("search", help="Search models")
    search_p.add_argument("query", help="Search query")
    search_p.add_argument("--format", choices=["human", "json"], default="human")

    # list
    list_p = sub.add_parser("list", help="List models")
    list_p.add_argument("--reactor", "--reactor-type", dest="reactor_type")
    list_p.add_argument("--code", "--physics-code", dest="physics_code")
    list_p.add_argument("--status")
    list_p.add_argument("--facility")
    list_p.add_argument("--format", choices=["human", "json"], default="human")

    # show
    show_p = sub.add_parser("show", help="Show model details")
    show_p.add_argument("model_id", help="Model identifier")
    show_p.add_argument("--format", choices=["human", "json"], default="human")

    # pull
    pull_p = sub.add_parser("pull", help="Download model")
    pull_p.add_argument("model_id", help="Model identifier")
    pull_p.add_argument("dest", nargs="?", default=".", help="Destination directory")
    pull_p.add_argument("--version", help="Specific version to pull")
    pull_p.add_argument("--open", action="store_true", help="Open in editor after download")

    # lineage
    lin_p = sub.add_parser("lineage", help="Show ROM → physics model chain")
    lin_p.add_argument("model_id", help="Model identifier")
    lin_p.add_argument("--format", choices=["human", "json"], default="human")

    # clone
    clone_p = sub.add_parser("clone", help="Clone a model for editing (creates fork)")
    clone_p.add_argument("model_id", help="Model to clone")
    clone_p.add_argument("--name", help="New model name (auto-generated if omitted)")
    clone_p.add_argument("--no-open", action="store_true", help="Don't open in editor")

    # diff
    diff_p = sub.add_parser("diff", help="Compare two model versions")
    diff_p.add_argument("model_a", help="First model (model_id or model_id@version)")
    diff_p.add_argument("model_b", help="Second model")

    # export
    export_p = sub.add_parser("export", help="Export model as ZIP")
    export_p.add_argument("model_id", help="Model identifier")
    export_p.add_argument("--output", "-o", help="Output file path")

    # audit
    audit_p = sub.add_parser("audit", help="View change history")
    audit_p.add_argument("--since", help="Show changes since date (ISO 8601)")
    audit_p.add_argument("--model", dest="model_id", help="Filter by model")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.action:
        parser.print_help()
        return 1

    handlers = {
        "init": _cmd_init,
        "validate": _cmd_validate,
        "add": _cmd_add,
        "clone": _cmd_clone,
        "search": _cmd_search,
        "list": _cmd_list,
        "show": _cmd_show,
        "pull": _cmd_pull,
        "lineage": _cmd_lineage,
        "diff": _cmd_diff,
        "export": _cmd_export,
        "audit": _cmd_audit,
    }

    handler = handlers.get(args.action)
    if handler is None:
        parser.print_help()
        return 1

    return handler(args)


# ---------------------------------------------------------------------------
# Command handlers
# ---------------------------------------------------------------------------


def _cmd_init(args) -> int:
    from pathlib import Path

    from neutron_os.extensions.builtins.model_corral.commands.init import model_init

    try:
        model_dir = model_init(
            args.name,
            reactor_type=args.reactor_type or "custom",
            physics_code=args.physics_code or "MCNP",
            facility=getattr(args, "facility", "") or "",
            output_dir=Path.cwd(),
        )
        print(f"Created: {model_dir}/")
        print("\nNext steps:")
        print(f"  1. Add your input files to {model_dir}/")
        print(f"  2. Edit {model_dir}/model.yaml (fill in description, facility, tags)")
        print(f"  3. Run: neut model validate {model_dir}")
        print(f"  4. Run: neut model add {model_dir}")

        # Open in editor if available
        _open_in_editor(model_dir)
        return 0
    except (ValueError, FileExistsError) as e:
        print(f"Error: {e}")
        return 1


def _cmd_validate(args) -> int:
    from neutron_os.extensions.builtins.model_corral.commands.validate import cmd_validate

    return cmd_validate(args.path, output_format=getattr(args, "format", "human"))


def _cmd_add(args) -> int:
    from pathlib import Path

    svc = _get_service()
    result = svc.add(Path(args.path), message=getattr(args, "message", ""))
    if result.success:
        print(f"Added: {result.model_id} v{result.version}")
        return 0
    print(f"Error: {result.error}")
    return 1


def _cmd_clone(args) -> int:
    from pathlib import Path

    from neutron_os.extensions.builtins.model_corral.commands.clone import model_clone

    svc = _get_service()
    try:
        clone_dir = model_clone(
            args.model_id,
            svc,
            new_name=getattr(args, "name", "") or "",
            output_dir=Path.cwd(),
        )
        print(f"Cloned: {clone_dir}/")
        print(f"  Forked from: {args.model_id}")
        print("\nNext steps:")
        print("  1. Edit your files and model.yaml")
        print(f"  2. Run: neut model validate {clone_dir}")
        print(f"  3. Run: neut model add {clone_dir}")

        if not getattr(args, "no_open", False):
            _open_in_editor(clone_dir)
        return 0
    except (FileExistsError, RuntimeError) as e:
        print(f"Error: {e}")
        return 1


def _cmd_search(args) -> int:
    svc = _get_service()
    results = svc.search(args.query)

    if getattr(args, "format", "human") == "json":
        print(json.dumps(results, indent=2))
    elif not results:
        print("No models found.")
    else:
        print(f"Found {len(results)} model(s):\n")
        for m in results:
            status = m.get("status", "")
            print(f"  {m['model_id']:<40} {m['reactor_type']:<8} {m['physics_code']:<8} {status}")
    return 0


def _cmd_list(args) -> int:
    svc = _get_service()
    models = svc.list_models(
        reactor_type=getattr(args, "reactor_type", None),
        physics_code=getattr(args, "physics_code", None),
        status=getattr(args, "status", None),
        facility=getattr(args, "facility", None),
    )

    if getattr(args, "format", "human") == "json":
        print(json.dumps(models, indent=2))
    elif not models:
        print("No models in registry.")
    else:
        print(f"{'Model ID':<40} {'Reactor':<8} {'Code':<8} {'Status':<12} {'Facility'}")
        print("-" * 80)
        for m in models:
            print(
                f"{m['model_id']:<40} {m['reactor_type']:<8} {m['physics_code']:<8} "
                f"{m['status']:<12} {m.get('facility', '')}"
            )
    return 0


def _cmd_show(args) -> int:
    svc = _get_service()
    info = svc.show(args.model_id)
    if info is None:
        print(f"Model not found: {args.model_id}")
        return 1

    if getattr(args, "format", "human") == "json":
        print(json.dumps(info, indent=2, default=str))
    else:
        print(f"Model: {info['model_id']}")
        print(f"  Name:         {info['name']}")
        print(f"  Reactor:      {info['reactor_type']}")
        print(f"  Code:         {info['physics_code']}")
        print(f"  Status:       {info['status']}")
        print(f"  Access:       {info['access_tier']}")
        print(f"  Facility:     {info.get('facility', '')}")
        print(f"  Created by:   {info['created_by']}")
        if info.get("description"):
            print(f"  Description:  {info['description'][:100]}")
        if info.get("tags"):
            print(f"  Tags:         {', '.join(info['tags'])}")
        if info.get("versions"):
            print(f"\n  Versions ({len(info['versions'])}):")
            for v in info["versions"]:
                print(
                    f"    v{v['version']}  {v.get('created_by', '')}  {v.get('checksum', '')[:12]}..."
                )
    return 0


def _cmd_pull(args) -> int:
    from pathlib import Path

    svc = _get_service()
    dest = Path(args.dest) / args.model_id
    result = svc.pull(args.model_id, dest, version=getattr(args, "version", None))
    if result.success:
        print(f"Downloaded to: {dest}")
        if getattr(args, "open", False):
            _open_in_editor(dest)
        return 0
    print(f"Error: {result.error}")
    return 1


def _cmd_lineage(args) -> int:
    svc = _get_service()
    chain = svc.lineage(args.model_id)

    if getattr(args, "format", "human") == "json":
        print(json.dumps(chain, indent=2))
    elif not chain:
        print(f"{args.model_id}: no parent models (root)")
    else:
        print(f"Lineage for {args.model_id}:")
        for entry in chain:
            print(f"  <- {entry['parent_model_id']} ({entry['relationship_type']})")
    return 0


def _cmd_diff(args) -> int:
    import difflib
    import tempfile
    from pathlib import Path

    svc = _get_service()
    a = svc.show(args.model_a)
    b = svc.show(args.model_b)

    if a is None:
        print(f"Model not found: {args.model_a}")
        return 1
    if b is None:
        print(f"Model not found: {args.model_b}")
        return 1

    # Pull both to temp dirs for full diff
    with tempfile.TemporaryDirectory() as tmp:
        dir_a = Path(tmp) / "a"
        dir_b = Path(tmp) / "b"
        res_a = svc.pull(args.model_a, dir_a)
        res_b = svc.pull(args.model_b, dir_b)

        if not res_a.success or not res_b.success:
            # Fall back to metadata diff
            print(f"Comparing metadata: {args.model_a} vs {args.model_b}\n")
            _diff_metadata(a, b)
            return 0

        # Diff model.yaml (the most important file)
        yaml_a = (dir_a / "model.yaml").read_text() if (dir_a / "model.yaml").exists() else ""
        yaml_b = (dir_b / "model.yaml").read_text() if (dir_b / "model.yaml").exists() else ""

        if yaml_a != yaml_b:
            print(f"--- {args.model_a}/model.yaml")
            print(f"+++ {args.model_b}/model.yaml")
            diff = difflib.unified_diff(
                yaml_a.splitlines(keepends=True),
                yaml_b.splitlines(keepends=True),
                fromfile=args.model_a,
                tofile=args.model_b,
            )
            for line in diff:
                if line.startswith("+") and not line.startswith("+++"):
                    print(f"\033[32m{line}\033[0m", end="")
                elif line.startswith("-") and not line.startswith("---"):
                    print(f"\033[31m{line}\033[0m", end="")
                else:
                    print(line, end="")
            print()

        # Show files that differ or are only in one
        files_a = {str(f.relative_to(dir_a)) for f in dir_a.rglob("*") if f.is_file()}
        files_b = {str(f.relative_to(dir_b)) for f in dir_b.rglob("*") if f.is_file()}

        only_a = files_a - files_b
        only_b = files_b - files_a

        if only_a:
            print(f"Only in {args.model_a}:")
            for f in sorted(only_a):
                print(f"  - {f}")
        if only_b:
            print(f"Only in {args.model_b}:")
            for f in sorted(only_b):
                print(f"  + {f}")

        if yaml_a == yaml_b and not only_a and not only_b:
            print("No differences found.")

    return 0


def _diff_metadata(a: dict, b: dict) -> None:
    """Fallback metadata-only diff."""
    fields = [
        "reactor_type",
        "physics_code",
        "status",
        "facility",
        "access_tier",
        "description",
        "created_by",
    ]
    changed = False
    for field in fields:
        va = a.get(field, "")
        vb = b.get(field, "")
        if va != vb:
            changed = True
            print(f"  {field}:")
            print(f"    \033[31m- {va}\033[0m")
            print(f"    \033[32m+ {vb}\033[0m")
    if not changed:
        print("  No metadata differences.")


def _cmd_export(args) -> int:
    import shutil
    import tempfile
    from pathlib import Path

    svc = _get_service()
    with tempfile.TemporaryDirectory() as tmp:
        dest = Path(tmp) / args.model_id
        result = svc.pull(args.model_id, dest)
        if not result.success:
            print(f"Error: {result.error}")
            return 1

        output = getattr(args, "output", None) or f"{args.model_id}.zip"
        output = output.removesuffix(".zip")
        shutil.make_archive(output, "zip", dest)
        print(f"Exported: {output}.zip")
    return 0


def _cmd_audit(args) -> int:
    svc = _get_service()
    # Simple audit — list all versions with timestamps
    models = svc.list_models()
    if not models:
        print("No models in registry.")
        return 0

    print(f"{'Model ID':<40} {'Version':<10} {'Created By':<25} {'Checksum'}")
    print("-" * 90)
    for m in models:
        info = svc.show(m["model_id"])
        if info and info.get("versions"):
            for v in info["versions"]:
                print(
                    f"{m['model_id']:<40} v{v['version']:<9} "
                    f"{v.get('created_by', ''):<25} {(v.get('checksum') or '')[:16]}"
                )
    return 0


def _open_in_editor(path) -> None:
    """Open a model directory in the user's preferred editor."""
    from axiom.infra.editor import open_in_editor

    editor = open_in_editor(path, file="model.yaml")
    if editor:
        print(f"\nOpened in {editor}.")


# ---------------------------------------------------------------------------
# Service factory
# ---------------------------------------------------------------------------


_SERVICE = None


def _get_service():
    """Get or create the ModelCorralService.

    Connects to the K3D PostgreSQL instance (same as EVE agent) and uses
    local filesystem storage. S3/SeaweedFS storage comes with Rascal (M3).

    DB URL resolution: AXIOM_DB_URL env var → default K3D PostgreSQL.
    """
    global _SERVICE
    if _SERVICE is not None:
        return _SERVICE

    import os

    from sqlalchemy import create_engine

    from axiom.infra.paths import get_user_state_dir
    from axiom.infra.storage import LocalStorageProvider
    from neutron_os.extensions.builtins.model_corral.db_models import Base
    from neutron_os.extensions.builtins.model_corral.service import ModelCorralService

    db_url = os.environ.get("AXIOM_DB_URL", "postgresql://axiom:axiom@localhost:5432/axiom_db")
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

    state_dir = get_user_state_dir()
    storage = LocalStorageProvider({"base_dir": str(state_dir / "model-storage")})

    _SERVICE = ModelCorralService(engine=engine, storage=storage)
    return _SERVICE


if __name__ == "__main__":
    sys.exit(main())
