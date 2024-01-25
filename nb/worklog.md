---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.16.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

```{code-cell} ipython3
from pprint import pprint as pp
from pathlib import Path

from pychum.engine.orca._renderer import OrcaInputRenderer
from pychum.engine.orca.config_loader import ConfigLoader
```

```{code-cell} ipython3
aa=ConfigLoader(Path("../tests/test_orca/opt_scan.toml"))
```

```{code-cell} ipython3
ab=aa.load_config()
```

```{code-cell} ipython3
ac=OrcaInputRenderer(ab)
```

```{code-cell} ipython3
print(ac.render('base.jinja'))
```

```{code-cell} ipython3
aa.data
```

```{code-cell} ipython3

```
