import sys
import warnings
from pathlib import Path

from pychum.engine.orca.config_loader import ConfigLoader


def test_units_deprecated():
    sys.modules.pop("pychum.units", None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        import pychum.units as u

        assert any(issubclass(item.category, DeprecationWarning) for item in caught)
        assert u.ureg is None
        assert u.Q_ is None


def test_config_loader_toml():
    for path in Path("tests").rglob("*.toml"):
        cfg = ConfigLoader(str(path)).load_config()
        assert cfg is not None
