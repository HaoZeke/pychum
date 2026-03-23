import re
from pathlib import Path

from pychum.engine.orca._renderer import OrcaInputRenderer
from pychum.engine.orca.config_loader import ConfigLoader

_DATA_DIR = Path(__file__).parent / "test_extra"


# TODO(rg): Cuz the jinja has a weird whitespace character
def normalize_whitespace(text):
    return re.sub(r"\s+", " ", text).strip()


def test_extra_blocks_rendering():
    toml_file_path = _DATA_DIR / "extra.toml"
    config_loader = ConfigLoader(toml_file_path)
    orca_config = config_loader.load_config()
    renderer = OrcaInputRenderer(orca_config)
    result = renderer.render("base.jinja")
    expected_output = """!NEB
!UHF NOSOSCF ForceConv

%scf
maxiter 300
end

* xyzfile 0 1 h2_base.xyz"""

    assert normalize_whitespace(result) == normalize_whitespace(expected_output)
