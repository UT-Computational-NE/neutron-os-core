"""Tests for auto-add MCNP detection and context-aware path defaults."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from neutron_os.extensions.builtins.model_corral.commands.auto_add import (
    auto_add_mcnp,
    extract_mcnp_metadata,
    is_mcnp_file,
)

SAMPLE_MCNP = """\
NETL TRIGA Steady State k-eff calculation

c Cell cards
1  1  -6.0   -1 2 -3     imp:n=1  $ fuel
2  2  -0.998  1 -4 2 -3  imp:n=1  $ water
3  0          4:-2:3      imp:n=0  $ void

c Surface cards
1  cz  1.8256
2  pz  0.0
3  pz  38.1
4  cz  20.0

c Data cards
m1   92235.80c  3.44e-3  92238.80c  1.37e-2  $ UZrH fuel
     40090.80c  3.30e-2  1001.80c   5.55e-2
mt1  zr-h.40t
m2   1001.80c   6.67e-2  8016.80c   3.33e-2  $ water
mt2  lwtr.20t
"""


# ---------------------------------------------------------------------------
# is_mcnp_file
# ---------------------------------------------------------------------------


def test_is_mcnp_file_by_i_extension(tmp_path: Path) -> None:
    f = tmp_path / "input.i"
    f.write_text("title\n")
    assert is_mcnp_file(f) is True


def test_is_mcnp_file_by_inp_extension(tmp_path: Path) -> None:
    f = tmp_path / "deck.inp"
    f.write_text("title\n")
    assert is_mcnp_file(f) is True


def test_is_mcnp_file_by_mcnp_extension(tmp_path: Path) -> None:
    f = tmp_path / "run.mcnp"
    f.write_text("title\n")
    assert is_mcnp_file(f) is True


def test_is_mcnp_file_by_content(tmp_path: Path) -> None:
    f = tmp_path / "deck.txt"
    f.write_text("Title Card\n\nc Cell cards\n1  1  -1.0  -1\n")
    assert is_mcnp_file(f) is True


def test_is_mcnp_file_rejects_non_mcnp(tmp_path: Path) -> None:
    f = tmp_path / "readme.txt"
    f.write_text("This is a readme file\nwith multiple lines\nno blank second line")
    assert is_mcnp_file(f) is False


# ---------------------------------------------------------------------------
# extract_mcnp_metadata
# ---------------------------------------------------------------------------


def test_extract_title(tmp_path: Path) -> None:
    f = tmp_path / "input.i"
    f.write_text(SAMPLE_MCNP)
    meta = extract_mcnp_metadata(f)
    assert meta["title"] == "NETL TRIGA Steady State k-eff calculation"


def test_extract_material_numbers(tmp_path: Path) -> None:
    f = tmp_path / "input.i"
    f.write_text(SAMPLE_MCNP)
    meta = extract_mcnp_metadata(f)
    assert sorted(meta["material_numbers"]) == [1, 2]


def test_extract_sab_cards(tmp_path: Path) -> None:
    f = tmp_path / "input.i"
    f.write_text(SAMPLE_MCNP)
    meta = extract_mcnp_metadata(f)
    assert meta["has_sab"] is True


def test_extract_no_sab(tmp_path: Path) -> None:
    content = "Title\n\n1  1  -1.0  -1\n\n1  so  5.0\n\nm1  1001.80c  1.0\n"
    f = tmp_path / "input.i"
    f.write_text(content)
    meta = extract_mcnp_metadata(f)
    assert meta["has_sab"] is False


# ---------------------------------------------------------------------------
# auto_add_mcnp
# ---------------------------------------------------------------------------


def test_auto_add_creates_directory(tmp_path: Path) -> None:
    f = tmp_path / "triga_ss.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    assert model_dir.is_dir()
    assert model_dir.name == "triga-ss"


def test_auto_add_copies_input_file(tmp_path: Path) -> None:
    f = tmp_path / "triga_ss.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    assert (model_dir / "triga_ss.i").exists()
    assert (model_dir / "triga_ss.i").read_text() == SAMPLE_MCNP


def test_auto_add_generates_valid_model_yaml(tmp_path: Path) -> None:
    f = tmp_path / "triga_ss.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    manifest = yaml.safe_load((model_dir / "model.yaml").read_text())
    assert manifest["model_id"] == "triga-ss"
    assert manifest["physics_code"] == "MCNP"
    assert manifest["status"] == "draft"
    assert manifest["name"] == "NETL TRIGA Steady State k-eff calculation"
    assert "auto-registered" in manifest["tags"]
    assert manifest["input_files"][0]["path"] == "triga_ss.i"


def test_auto_add_sanitizes_kebab_case(tmp_path: Path) -> None:
    f = tmp_path / "My Complex___Model Name.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    assert model_dir.name == "my-complex-model-name"


def test_auto_add_short_name_gets_prefix(tmp_path: Path) -> None:
    f = tmp_path / "ab.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    assert model_dir.name == "model-ab"


def test_auto_add_detects_material_numbers(tmp_path: Path) -> None:
    f = tmp_path / "deck.i"
    f.write_text(SAMPLE_MCNP)
    model_dir = auto_add_mcnp(f)
    manifest = yaml.safe_load((model_dir / "model.yaml").read_text())
    assert manifest["_detected_material_numbers"] == [1, 2]


def test_auto_add_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        auto_add_mcnp(tmp_path / "nonexistent.i")


def test_auto_add_not_mcnp(tmp_path: Path) -> None:
    f = tmp_path / "readme.txt"
    f.write_text("This is not MCNP\nhas content\non multiple lines")
    with pytest.raises(ValueError, match="Not an MCNP file"):
        auto_add_mcnp(f)


def test_auto_add_collision_appends_date(tmp_path: Path) -> None:
    f = tmp_path / "deck.i"
    f.write_text(SAMPLE_MCNP)
    # Pre-create the directory to force collision
    (tmp_path / "deck").mkdir()
    model_dir = auto_add_mcnp(f)
    assert model_dir.name.startswith("deck-")
    assert model_dir.is_dir()


# ---------------------------------------------------------------------------
# Context-aware path defaults (CLI parser)
# ---------------------------------------------------------------------------


def test_validate_default_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["validate"])
    assert args.path == "."


def test_add_default_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["add"])
    assert args.path == "."


def test_generate_default_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["generate"])
    assert args.path == "."


def test_lint_default_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["lint"])
    assert args.path == "."


def test_sweep_default_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["sweep", "--param", "enrichment", "--values", "0.05,0.10"])
    assert args.path == "."


def test_validate_explicit_path() -> None:
    from neutron_os.extensions.builtins.model_corral.cli import build_parser

    parser = build_parser()
    args = parser.parse_args(["validate", "/some/path"])
    assert args.path == "/some/path"
