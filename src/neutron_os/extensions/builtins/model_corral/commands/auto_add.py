"""Auto-add -- register an MCNP input deck with minimal effort.

When the user runs ``neut model add ./input.i`` (a file, not a directory),
auto-creates a model directory, generates model.yaml from the deck,
and registers it.  One command, zero model.yaml authoring.
"""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import yaml

MCNP_EXTENSIONS = {".i", ".inp", ".mcnp"}


def is_mcnp_file(path: Path) -> bool:
    """Detect if a file is an MCNP input deck."""
    if path.suffix.lower() in MCNP_EXTENSIONS:
        return True
    # Check content: MCNP files have a title card on line 1,
    # then blank line, then cell cards
    try:
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()[:10]
        if len(lines) >= 3 and lines[1].strip() == "":
            return True  # title card + blank line pattern
    except Exception:
        pass
    return False


def extract_mcnp_metadata(path: Path) -> dict:
    """Extract metadata from an MCNP input deck.

    Returns dict with title, material_numbers, and any other detectable info.
    """
    content = path.read_text(encoding="utf-8", errors="ignore")
    lines = content.splitlines()

    metadata: dict = {
        "title": lines[0].strip() if lines else path.stem,
        "material_numbers": [],
        "has_sab": False,
    }

    # Find material card numbers (m1, m2, m10, etc.)
    mat_pattern = re.compile(r"^m(\d+)\s", re.IGNORECASE)
    sab_pattern = re.compile(r"^mt\d+\s", re.IGNORECASE)

    for line in lines:
        mat_match = mat_pattern.match(line)
        if mat_match:
            metadata["material_numbers"].append(int(mat_match.group(1)))
        if sab_pattern.match(line):
            metadata["has_sab"] = True

    return metadata


def auto_add_mcnp(
    file_path: Path,
    message: str = "",
    reactor_type: str = "custom",
    facility: str = "",
) -> Path:
    """Auto-create model directory from MCNP file and register it.

    Args:
        file_path: Path to MCNP input file.
        message: Commit message.
        reactor_type: Reactor type (auto-detected if possible).
        facility: Facility (auto-detected if possible).

    Returns:
        Path to created model directory.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not is_mcnp_file(file_path):
        raise ValueError(f"Not an MCNP file: {file_path}")

    # Extract metadata from the deck
    metadata = extract_mcnp_metadata(file_path)

    # Generate model_id from filename
    stem = file_path.stem.lower()
    # Sanitize to kebab-case
    model_id = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    if len(model_id) < 3:
        model_id = f"model-{model_id}"

    # Create model directory
    model_dir = file_path.parent / model_id
    if model_dir.exists():
        # Append timestamp to avoid collision
        model_dir = file_path.parent / f"{model_id}-{datetime.now(UTC).strftime('%Y%m%d')}"
    model_dir.mkdir(parents=True, exist_ok=True)

    # Copy input file
    dest_file = model_dir / file_path.name
    shutil.copy2(str(file_path), str(dest_file))

    # Auto-detect author
    author = ""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "user.email"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            author = result.stdout.strip()
    except Exception:
        pass
    author = author or "unknown@example.com"

    # Smart facility default
    if not facility:
        facility_defaults = {"TRIGA": "NETL", "MSR": "ORNL", "PWR": "generic"}
        facility = facility_defaults.get(reactor_type.upper(), "")

    # Build model.yaml
    manifest: dict = {
        "model_id": model_id,
        "name": (
            metadata["title"][:80] if metadata["title"] else model_id.replace("-", " ").title()
        ),
        "version": "0.1.0",
        "status": "draft",
        "reactor_type": reactor_type,
        "facility": facility or "unknown",
        "physics_code": "MCNP",
        "physics_domain": ["neutronics"],
        "created_by": author,
        "created_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "access_tier": "facility",
        "description": f"{metadata['title']} — auto-registered from {file_path.name}",
        "tags": ["auto-registered"],
        "input_files": [{"path": file_path.name, "format": "mcnp"}],
    }

    # Add detected materials
    if metadata["material_numbers"]:
        manifest["_detected_material_numbers"] = sorted(metadata["material_numbers"])

    (model_dir / "model.yaml").write_text(
        yaml.dump(manifest, default_flow_style=False, sort_keys=False),
        encoding="utf-8",
    )

    return model_dir
