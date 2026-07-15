import importlib.util
import sys
import warnings
from pathlib import Path


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_units_deprecated():
    root = Path(__file__).resolve().parents[1] / "pychum" / "units.py"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        # load as package path
        sys.modules.pop("pychum.units", None)
        import pychum.units as u

        assert any(issubclass(x.category, DeprecationWarning) for x in w)
        assert u.ureg is None


def test_config_loader_toml():
    from pychum.engine.orca.config_loader import ConfigLoader

    for f in Path("tests").rglob("*.toml"):
        cfg = ConfigLoader(str(f)).load_config()
        assert cfg is not None
