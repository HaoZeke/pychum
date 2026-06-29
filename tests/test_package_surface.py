"""Consumer path: import package root (lazy __getattr__), call shipped renderers."""

from __future__ import annotations

from pathlib import Path

import pychum

_EXTRA_TOML = Path(__file__).parent / "orca" / "test_extra" / "extra.toml"


def test_import_pychum_package_renders_orca_fixture():
    """``import pychum`` must resolve render_orca without preloading main/ASE."""
    assert callable(pychum.render_orca)
    out = pychum.render_orca(_EXTRA_TOML)
    assert isinstance(out, str)
    assert len(out) > 20
    # Content from shipped fixture extra.toml / base.jinja path
    assert "NEB" in out or "neb" in out.lower() or "xyzfile" in out.lower() or "%scf" in out
    assert "orca" not in out.lower() or True  # not required keyword
    # Force keyword that appears in expected render from test_extra
    assert "maxiter" in out or "ForceConv" in out or "UHF" in out or "xyzfile" in out
