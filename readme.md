
# Table of Contents

-   [About](#org476f174)
    -   [Features](#org0168ce7)
        -   [Supported Engines](#org24b6ad5)
    -   [Rationale](#org49cd152)
-   [Usage](#org4a4d3d9)
-   [Development](#org7fadd95)
    -   [Adding ORCA blocks](#org70cb903)
    -   [Documentation](#org86de685)
        -   [Readme](#org9468810)
-   [License](#orgc959d45)



<a id="org476f174"></a>

# About

![img](branding/logo/pychum_logo.png)

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)

A **pure-python** project to generate input files for various common
computational chemistry workflows. This means:

-   Generating input structures for `jobflow` / Fireworks
    -   From unified `toml` inputs

This is a spin-off from `wailord` ([here](https://wailord.xyz)) which is meant to handle aggregated
runs in a specific workflow, while `pychum` is meant to generate **single runs**.
It is also a companion to `chemparseplot` ([here](https://github.com/haoZeke/chemparseplot)) which is meant to provide
uniform visualizations for the outputs of various computational chemistry
programs.


<a id="org0168ce7"></a>

## Features

-   Jobflow support
    -   Along with Fireworks
-   Unit aware conversions
    -   Via `pint`


<a id="org24b6ad5"></a>

### Supported Engines

-   NEB calculations
    -   ORCA
    -   EON
-   Single point calculations
    -   ORCA
    -   EON


<a id="org49cd152"></a>

## Rationale

I needed to run a bunch of systems. `jobflow` / Fireworks / AiiDA were ideal,
until I realized only VASP is really well supported by them.


<a id="org4a4d3d9"></a>

# Usage

The simplest usage is via the CLI:

    python -m pychum.cli


<a id="org7fadd95"></a>

# Development

Before writing tests and incorporating the functions into the CLI it is helpful
to often visualize the intermediate steps. For this we can setup a complete
development environment including the notebook server.

    pixi shell
    pdm sync
    pdm run $SHELL
    jupyter lab --ServerApp.allow_remote_access=1 \
        --ServerApp.open_browser=False --port=8889

Then go through the `nb` folder notebooks.


<a id="org70cb903"></a>

## Adding ORCA blocks

Changes are to be made in the following files under the `pychum/engine/orca/` folder:

-   The relevant `.jinja` file in the `_blocks` directory
-   The configuration loading mechanism in `config_loader.py`
-   The `dataclasses` folder
-   A sample test `.toml` file under `tests/test_orca`

While working on this, it may be instructive to use the `nb` folder notebooks.
Also all PRs must include a full test suite for the new blocks.


<a id="org86de685"></a>

## Documentation


<a id="org9468810"></a>

### Readme

The `readme` can be constructed via:

    ./scripts/org_to_md.sh readme_src.org readme.md


<a id="orgc959d45"></a>

# License

MIT. However, this is an academic resource, so **please cite** as much as possible
via:

-   The Zenodo DOI for general use.
-   The `wailord` paper for ORCA usage

