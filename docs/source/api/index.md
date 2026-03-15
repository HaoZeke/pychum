# API Reference

This section provides the complete API reference for pychum.

```{toctree}
:maxdepth: 2
:caption: Contents:

api/pychum
api/pychum.engine.orca
api/pychum.engine.eon
```

## Quick Reference

### Main Functions

```python
from pychum import render_orca, render_nwchem
from pathlib import Path

# Render ORCA input from TOML config
orca_input = render_orca(Path("config.toml"))

# Render NWChem input for eOn socket
nwchem_input = render_nwchem(
    pos_file=Path("geometry.xyz"),
    settings_path=Path("nwchem_settings.toml"),
    socket_address="127.0.0.1:8888",
    unix_mode=False,
    mem_in_gb=4,
)
```

### ORCA Engine

```python
from pychum.engine.orca import ConfigLoader, OrcaInputRenderer

# Load configuration from TOML
loader = ConfigLoader("config.toml")
config = loader.load_config()

# Render ORCA input
renderer = OrcaInputRenderer(config)
orca_input = renderer.render("base.jinja")
```

### EON Engine

```python
from pychum.engine.eon import NWChemRenderer, NWChemSocketConfig
from ase.io import read

# Read geometry
atoms = read("geometry.xyz")

# Create NWChem socket config
nw_config = NWChemSocketConfig(
    atoms=[...],  # List of NWChemAtom
    settings_path=Path("settings.toml"),
    socket_address="127.0.0.1:8888",
    unix_mode=False,
    mem_in_gb=4,
)

# Render NWChem input
renderer = NWChemRenderer(nw_config)
nwchem_input = renderer.render("nwchem_socket.jinja")
```

### Units

```python
from pychum.units import ureg

# Convert distance
distance = 1.5 * ureg.angstrom
print(distance.to(ureg.bohr))  # 2.8346 bohr

# Convert energy
energy = -76.0 * ureg.hartree
print(energy.to(ureg.kcal / ureg.mol))  # -47690.7 kcal/mol
```
