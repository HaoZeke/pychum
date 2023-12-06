
# Table of Contents

-   [About](#org82157d6)
    -   [Features](#org1fbffca)
        -   [Supported Engines](#org766b50a)
    -   [Rationale](#org15ffdd1)
-   [License](#org9b3f6a1)



<a id="org82157d6"></a>

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


<a id="org1fbffca"></a>

## Features

-   Jobflow support
    -   Along with Fireworks
-   Unit aware conversions
    -   Via `pint`


<a id="org766b50a"></a>

### Supported Engines

-   NEB calculations
    -   ORCA
    -   EON
-   Single point calculations
    -   ORCA
    -   EON


<a id="org15ffdd1"></a>

## Rationale

I needed to run a bunch of systems. `jobflow` / Fireworks / AiiDA were ideal,
until I realized only VASP is really well supported by them.


<a id="org9b3f6a1"></a>

# License

MIT. However, this is an academic resource, so **please cite** as much as possible
via:

-   The Zenodo DOI for general use.
-   The `wailord` paper for ORCA usage

