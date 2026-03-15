# ORCA Engine

```{eval-rst}
.. automodule:: pychum.engine.orca
   :members:
   :undoc-members:
   :show-inheritance:
```

## ConfigLoader

```{eval-rst}
.. autoclass:: pychum.engine.orca.ConfigLoader
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   ```python
   from pychum.engine.orca import ConfigLoader

   loader = ConfigLoader("config.toml")
   config = loader.load_config()
   ```
```

## OrcaInputRenderer

```{eval-rst}
.. autoclass:: pychum.engine.orca.OrcaInputRenderer
   :members:
   :undoc-members:
   :show-inheritance:

   Example usage:

   ```python
   from pychum.engine.orca import OrcaInputRenderer

   renderer = OrcaInputRenderer(config)
   orca_input = renderer.render("base.jinja")
   ```
```

## Data Classes

### OrcaConfig

```{eval-rst}
.. autoclass:: pychum.engine.orca.OrcaConfig
   :members:
   :undoc-members:
```

### NebBlock

```{eval-rst}
.. autoclass:: pychum.engine.orca.NebBlock
   :members:
   :undoc-members:
```

### GeomBlock

```{eval-rst}
.. autoclass:: pychum.engine.orca.GeomBlock
   :members:
   :undoc-members:
```

## Example TOML Configuration

```toml
[orca]
functional = "PBE0"
basis = "def2-SVP"

[coords]
charge = 0
multiplicity = 1
fmt = "xyz"

[[coords.atoms]]
symbol = "O"
x = 0.0
y = 0.0
z = 0.0

[[coords.atoms]]
symbol = "H"
x = 0.757
y = 0.586
z = 0.0

[[coords.atoms]]
symbol = "H"
x = -0.757
y = 0.586
z = 0.0

[scf]
max_iter = 100
```
