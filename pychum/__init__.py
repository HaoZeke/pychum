"""pychum public API with deferred engine imports."""

from __future__ import annotations

import importlib
from typing import TYPE_CHECKING, Any

__all__ = ["render_nwchem", "render_orca"]

if TYPE_CHECKING:
    from pychum.main import render_nwchem, render_orca


def __getattr__(name: str) -> Any:
    if name in ("render_orca", "render_nwchem"):
        main = importlib.import_module("pychum.main")
        return getattr(main, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
