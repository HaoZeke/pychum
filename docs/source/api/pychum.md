# pychum Package

```{eval-rst}
.. automodule:: pychum
   :members:
   :undoc-members:
   :show-inheritance:
```

## Functions

### render_orca

```{eval-rst}
.. autofunction:: pychum.render_orca
```

### render_nwchem

```{eval-rst}
.. autofunction:: pychum.render_nwchem
```

## Example Usage

```python
from pychum import render_orca, render_nwchem
from pathlib import Path

# Generate ORCA input
orca_input = render_orca(Path("orca_config.toml"))
with open("calculation.inp", "w") as f:
    f.write(orca_input)

# Generate NWChem input for eOn
nwchem_input = render_nwchem(
    pos_file=Path("molecule.xyz"),
    settings_path=Path("nwchem.toml"),
    socket_address="127.0.0.1:8888",
    unix_mode=False,
    mem_in_gb=4,
)
```
