# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# -- Project information -----------------------------------------------------
project = "pychum"
copyright = "2026, Rohit Goswami"
author = "Rohit Goswami"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "myst_nb",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for autodoc -----------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# -- Options for intersphinx -------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "ase": ("https://wiki.fysik.dtu.dk/ase/", None),
    # Link to other rgpkgs packages
    "rgpycrumbs": ("https://rgpycrumbs.rgoswami.me", None),
    "chemparseplot": ("https://chemparseplot.rgoswami.me", None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = "shibuya"
html_static_path = ["_static"]
html_title = "pychum"

# -- Options for MyST-NB -----------------------------------------------------
nb_execution_mode = "off"
