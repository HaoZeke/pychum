# SPDX-FileCopyrightText: 2023-present Rohit Goswami <rog32@hi.is>
#
# SPDX-License-Identifier: MIT
"""Unit registry for pychum (pint), aligned with chemparseplot energy defs.

Uses ``cache_folder=None`` to avoid flexcache path bleed across environments.
Lazy construction so ``import pychum`` stays light until units are used.
"""

from __future__ import annotations

import warnings
from typing import Any

__all__ = ["Q_", "ureg"]

_ureg = None
_Q = None


def _ensure_registry():
    global _ureg, _Q
    if _ureg is not None:
        return _ureg, _Q
    import pint

    _ureg = pint.UnitRegistry(cache_folder=None)
    _ureg.define("kcal_mol = kcal / 6.02214076e+23 = kcm")
    # Same chemical-energy presentation dimension as chemparseplot.units
    _ureg.define("chem_eV = [chem_energy]")
    _ureg.define("chem_kcal_mol = 23.06054783061903 * chem_eV")
    _ureg.define("chem_kJ_mol = 96.48533212331002 * chem_eV")
    _Q = _ureg.Quantity
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        _Q([])
    return _ureg, _Q


def __getattr__(name: str) -> Any:
    if name == "ureg":
        ureg, _ = _ensure_registry()
        return ureg
    if name == "Q_":
        _, Q = _ensure_registry()
        return Q
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
