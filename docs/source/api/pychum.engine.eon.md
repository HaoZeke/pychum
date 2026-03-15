# EON Engine

```{eval-rst}
.. automodule:: pychum.engine.eon
   :members:
   :undoc-members:
   :show-inheritance:
```

## NWChemSocketConfig

```{eval-rst}
.. autoclass:: pychum.engine.eon.NWChemSocketConfig
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   ```python
   from pychum.engine.eon import NWChemSocketConfig, NWChemAtom

   atoms = [
       NWChemAtom(symbol="O", x=0.0, y=0.0, z=0.0),
       NWChemAtom(symbol="H", x=0.757, y=0.586, z=0.0),
       NWChemAtom(symbol="H", x=-0.757, y=0.586, z=0.0),
   ]

   config = NWChemSocketConfig(
       atoms=atoms,
       settings_path=Path("nwchem.toml"),
       socket_address="127.0.0.1:8888",
       unix_mode=False,
       mem_in_gb=4,
   )
   ```
```

## NWChemRenderer

```{eval-rst}
.. autoclass:: pychum.engine.eon.NWChemRenderer
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   ```python
   from pychum.engine.eon import NWChemRenderer

   renderer = NWChemRenderer(config)
   nwchem_input = renderer.render("nwchem_socket.jinja")
   ```
```

## NWChemAtom

```{eval-rst}
.. autoclass:: pychum.engine.eon.NWChemAtom
   :members:
   :undoc-members:
```

## Example TOML Settings

```toml
[nwchem]
task = "energy"
theory = "dft"

[dft]
functional = "b3lyp"

[basis]
type = "6-31g*"

[scf]
max_iter = 100
```
