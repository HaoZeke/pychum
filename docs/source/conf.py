import os
import sys

# -- Path setup --------------------------------------------------------------
sys.path.insert(0, os.path.abspath("../../pychum"))

# -- Project information -----------------------------------------------------
project = "pychum"
project_copyright = "2026, Rohit Goswami"
author = "Rohit Goswami"
# html_logo = "../../branding/logo/pychum_logo.png"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinxcontrib.programoutput",  # Runs 'uv run ...' for dynamic examples
    # Include autodoc since sphinx-click relies on its mocking machinery.
    "sphinx.ext.autodoc",  # Needed for mocking machinery
    "sphinx.ext.viewcode",  # Adds '[source]' links
    "sphinx.ext.intersphinx",
    "autoapi.extension",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx_sitemap",
]

templates_path = ["_templates"]
exclude_patterns = []

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "rgpycrumbs": ("https://rgpycrumbs.rgoswami.me", None),
}

# -- Mocking Dependencies ----------------------------------------------------
autodoc_mock_imports = [
    "numpy",
    "ase",
    "rich",
    "jinja2",
    "tomli",
    "chemparseplot",
    "rgpycrumbs",
]

# -- Options for HTML output -------------------------------------------------
html_theme = "shibuya"
html_static_path = ["_static"]

# Shibuya theme specific options
html_theme_options = {
    "github_url": "https://github.com/HaoZeke/pychum",
    "nav_links": [
        {
            "title": "Ecosystem",
            "children": [
                {
                    "title": "rgpycrumbs",
                    "url": "https://rgpycrumbs.rgoswami.me",
                    "summary": "CLI suite hub, surfaces, eOn plot dispatch",
                    "external": True,
                },
                {
                    "title": "chemparseplot",
                    "url": "https://chemparseplot.rgoswami.me",
                    "summary": "Parse + plot (ORCA / eOn / CON)",
                    "external": True,
                },
                {
                    "title": "eOn",
                    "url": "https://eondocs.org",
                    "summary": "Long-timescale MD / NEB engine",
                    "external": True,
                },
                {
                    "title": "readcon-core",
                    "url": "https://github.com/lode-org/readcon-core",
                    "summary": "CON/convel I/O (Rust core; PyPI: readcon)",
                    "external": True,
                },
            ],
        },
    ],
}

autoapi_dirs = ["../../pychum"]
html_baseurl = "https://pychum.rgoswami.me"
