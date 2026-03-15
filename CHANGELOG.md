# Changelog

<!-- towncrier release notes start -->

## [1.4.0](https://github.com/HaoZeke/pychum/tree/1.4.0) - 2026-03-15

### Added

- Diataxis documentation structure: tutorial, API reference (autodoc), developer guides
(dataclasses, templates, validators, ORCA blocks), how-to guides, and reference (glossary).
Switched to shibuya Sphinx theme. ([#docs_tutorials](https://github.com/HaoZeke/pychum/issues/docs_tutorials))


## v1.1.0 - 2026-02-21

### Added

- `uv`-first development workflow, replacing PDM.
- Core dependencies on `rgpycrumbs>=1.1.0` and `chemparseplot>=1.1.0`.
- Standard optional dependency groups for `test`, `lint`, `cli`, and `doc`.

### Changed

- Renamed package and all internal imports back to `pychum` (from `pychumpchem`) for PyPI consistency.
- Updated ORCA input templates and test expectations for NEB blocks.
- Synchronized project version to `1.1.0` across `pixi.toml` and metadata.

### Fixed

- Coverage path configurations in `pyproject.toml`.
- Mass-corrected all legacy `pychum` imports in tests and notebooks.
