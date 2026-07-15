# SPDX-FileCopyrightText: 2023-present Rohit Goswami <rog32@hi.is>
#
# SPDX-License-Identifier: MIT
"""Deprecated unit registry stub.

pychum is an input generator and does not own physical unit conversion.
Use ``chemparseplot.units`` (rgpkgs suite owner) for pint quantities.

This module no longer constructs a second ``UnitRegistry``.
"""

from __future__ import annotations

import warnings

warnings.warn(
    "pychum.units is deprecated and no longer provides a UnitRegistry. "
    "Use chemparseplot.units (ureg, Q_) for suite unit conversion.",
    DeprecationWarning,
    stacklevel=2,
)

ureg = None  # type: ignore[assignment]
Q_ = None  # type: ignore[assignment]

__all__ = ["Q_", "ureg"]
