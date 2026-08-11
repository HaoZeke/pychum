# Configuration file for the Sphinx documentation builder.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

project = "pychum"
copyright = "2026, Rohit Goswami"
author = "Rohit Goswami"
html_title = "pychum documentation"
html_logo = "../../branding/logo/pychum_logo.png"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_sitemap",
    "sphinxcontrib.mermaid",
    "autoapi.extension",
    "myst_nb",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "api"]

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autoapi_dirs = ["../../pychum"]
autoapi_keep_files = False

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "ase": ("https://wiki.fysik.dtu.dk/ase/", None),
    "rgpycrumbs": ("https://rgpycrumbs.rgoswami.me", None),
    "chemparseplot": ("https://chemparseplot.rgoswami.me", None),
    "eon": ("https://eondocs.org", None),
}

myst_enable_extensions = ["colon_fence", "deflist"]
nb_execution_mode = "off"
mermaid_version = "11.4.0"
mermaid_init_js = "mermaid.initialize({startOnLoad:true, theme:'neutral'});"

html_theme = "shibuya"
html_static_path = ["_static"]
html_extra_path = ["llms.txt"]
html_baseurl = "https://pychum.rgoswami.me/"

html_context = {
    "source_type": "github",
    "source_user": "HaoZeke",
    "source_repo": "pychum",
    "source_version": "main",
    "source_docs_path": "/docs/orgmode/",
}

html_sidebars = {
    "**": [
        "sidebars/localtoc.html",
        "sidebars/repo-stats.html",
        "sidebars/edit-this-page.html",
    ],
}

html_theme_options = {
    "github_url": "https://github.com/HaoZeke/pychum",
    "accent_color": "rose",
    "dark_code": True,
    "globaltoc_expand_depth": 1,
    "toctree_collapse": True,
    "toctree_maxdepth": 3,
    "toctree_titles_only": True,
    "nav_links": [
        {
            "title": "Ecosystem",
            "children": [
                {
                    "title": "rgpycrumbs",
                    "url": "https://rgpycrumbs.rgoswami.me",
                    "summary": "Core types, surfaces, and CLI dispatcher",
                    "external": True,
                },
                {
                    "title": "chemparseplot",
                    "url": "https://chemparseplot.rgoswami.me",
                    "summary": "Parsers and publication plots",
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
        {
            "title": "PyPI",
            "url": "https://pypi.org/project/pychum/",
            "external": True,
        },
    ],
}

copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d*\]: | {2,5}\.\.\.: | {5,8}: "
copybutton_prompt_is_regexp = True
copybutton_exclude = ".linenos, .gp, .go"
