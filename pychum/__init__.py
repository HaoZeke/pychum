"""pychum public API with deferred engine imports.

``render_orca`` / ``render_nwchem`` stay available as attributes; ASE and
renderer stacks load only when a render function is first used.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

__all__ = ["render_nwchem", "render_orca"]

if TYPE_CHECKING:
    from pychum.main import render_nwchem, render_orca


def __getattr__(name: str) -> Any:
    if name in ("render_orca", "render_nwchem"):
        from pychum import main as _main

        return getattr(_main, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
