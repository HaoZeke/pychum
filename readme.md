
# Table of Contents

-   [About](#orgf82c3d6)
    -   [Ecosystem Overview](#org1ef5b99)
    -   [Features](#orgd7f6835)
        -   [Supported Engines](#org6e22848)
    -   [Rationale](#org5ac5dff)
-   [Usage](#orgde48b7e)
-   [Development](#org60cabf4)
    -   [Adding ORCA blocks](#org4153b25)
    -   [Documentation](#org721896a)
        -   [Readme](#orga426038)
-   [License](#org33508b4)



<a id="orgf82c3d6"></a>

# About

![img](branding/logo/pychum_logo.png)

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

A **pure-python** project to generate input files for various common
computational chemistry workflows. This means:

-   Generating input structures for `jobflow` / Fireworks
    -   From unified `toml` inputs
-   ORCA blocks (NEB, geometry scans, extras) and eOn renderers via Jinja templates
-   Shared units and helpers with [`rgpycrumbs`](https://github.com/HaoZeke/rgpycrumbs) (`rgpycrumbs>=1.9.16`). Suite pins/config live in **rgpkgs** (`~/.config/rgpkgs/config.toml`, project `rgpkgs.toml`) — pychum does not define its own pin file

This is a spin-off from `wailord` ([here](https://wailord.xyz)). **Tool split:**

- **`pychum`** — sole path for **single-run input generation** (ORCA Jinja/TOML,
  NWChem socket for eOn). Prefer `pychum` over wailord `inpGenerator`.
- **`chemparseplot`** — sole path for **parsing and plotting outputs** (including
  ORCA NEB via a public API that may use OPI internally; do not depend on `opi`
  directly).
- **`wailord`** — optional **batch/experiment** orchestration only; should call
  pychum + chemparseplot rather than reimplement ORCA I/O.

It is a companion to [`chemparseplot`](https://github.com/HaoZeke/chemparseplot)
(v1.8+ recommended) for uniform visualizations of computational chemistry outputs. Install with `pip install pychum` (Python ≥3.10); develop with `pixi run -e test test` or `uv sync --extra test`.


<a id="org1ef5b99"></a>

## Ecosystem Overview

`pychum` is part of the `rgpycrumbs` suite of interlinked libraries.

![img](branding/logo/ecosystem.png)


<a id="orgd7f6835"></a>

## Features

-   Jobflow support
    -   Along with Fireworks
-   Unit aware conversions
    -   Via `pint`


<a id="org6e22848"></a>

### Supported Engines

-   NEB calculations
    -   ORCA
    -   EON
-   Single point calculations
    -   ORCA
    -   EON


<a id="org5ac5dff"></a>

## Rationale

I needed to run a bunch of systems. `jobflow` / Fireworks / AiiDA were ideal,
until I realized only VASP is really well supported by them.

Also there were some minor problems with the ORCA input parser&#x2026;

-   It chokes on multiple `#` symbols, so `# MaxIter 50 # something` will error
    out on `SOMETHING`
-   No real ordering or syntax highlighting in major IDEs

Along with other minor inconveniences which make for enough friction over time
to necessitate this library.


<a id="orgde48b7e"></a>

# Usage

The simplest usage is via the CLI:

    uv run pychum --help
    # Or alternatively
    python -m pychum.cli --help


<a id="org60cabf4"></a>

# Development

Before writing tests and incorporating the functions into the CLI it is helpful
to often visualize the intermediate steps. For this we can setup a complete
development environment including the notebook server.

    uv sync --all-extras
    uv run jupyter lab --ServerApp.allow_remote_access=1 \
        --ServerApp.open_browser=False --port=8889

Then go through the `nb` folder notebooks.


<a id="org4153b25"></a>

## Adding ORCA blocks

Changes are to be made in the following files under the `pychum/engine/orca/` folder:

-   The relevant `.jinja` file in the `_blocks` directory
-   The configuration loading mechanism in `config_loader.py`
-   The `dataclasses` folder
-   A sample test `.toml` file under `tests/test_orca`

While working on this, it may be instructive to use the `nb` folder notebooks.
Also all PRs must include a full test suite for the new blocks.


<a id="org721896a"></a>

## Documentation


<a id="orga426038"></a>

### Readme

The `readme` can be constructed via:

    ./scripts/org_to_md.sh readme_src.org readme.md


<a id="org33508b4"></a>

# License

MIT. However, this is an academic resource, so **please cite** as much as possible
via:

-   The Zenodo DOI for general use.
-   The `wailord` paper for ORCA usage
