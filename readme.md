
# Table of Contents

-   [About](#org7c77871)
    -   [Features](#org37bf279)
        -   [Supported Engines](#orge25642d)
    -   [Rationale](#orgb4f705c)
-   [Development](#orgaabb253)
    -   [Documentation](#orge72c445)
        -   [Readme](#org23ffec5)
-   [License](#org94f529f)



<a id="org7c77871"></a>

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


<a id="org37bf279"></a>

## Features

-   Jobflow support
    -   Along with Fireworks
-   Unit aware conversions
    -   Via `pint`


<a id="orge25642d"></a>

### Supported Engines

-   NEB calculations
    -   ORCA
    -   EON
-   Single point calculations
    -   ORCA
    -   EON


<a id="orgb4f705c"></a>

## Rationale

I needed to run a bunch of systems. `jobflow` / Fireworks / AiiDA were ideal,
until I realized only VASP is really well supported by them.


<a id="orgaabb253"></a>

# Development

Before writing tests and incorporating the functions into the CLI it is helpful
to often visualize the intermediate steps. For this we can setup a complete
development environment including the notebook server.

    pixi shell
    pdm sync
    pdm run jupyter lab --ServerApp.allow_remote_access=1 \
        --ServerApp.open_browser=False --port=8889

Then go through the `nb` folder notebooks.


<a id="orge72c445"></a>

## Documentation


<a id="org23ffec5"></a>

### Readme

The `readme` can be constructed via:

    ./scripts/org_to_md.sh readme_src.org readme.md


<a id="org94f529f"></a>

# License

MIT. However, this is an academic resource, so **please cite** as much as possible
via:

-   The Zenodo DOI for general use.
-   The `wailord` paper for ORCA usage

