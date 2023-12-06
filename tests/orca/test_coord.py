from pychum.engine.orca._dataclasses import Atom, OrcaConfig, Coords
from pychum.engine.orca._renderer import OrcaInputRenderer

# Helper function to create a config and render the template
def render_config(atoms, coord_type='xyz', charge=0, multiplicity=1):
    coords = Coords(charge=charge, multiplicity=multiplicity, atoms=atoms, fmt = coord_type)
    config = OrcaConfig(engine='orca', coords=coords)
    renderer = OrcaInputRenderer(config)
    return renderer.render('coord.jinja')

# Test case for standard atoms in xyz format
def test_standard_atoms_xyz():
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0), Atom(symbol='O', x=0.0, y=0.0, z=1.13)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.0 0.0 0.0\nO 0.0 0.0 1.13\n*"
    assert result.strip() == expected.strip()

# Test case for dummy atoms
def test_dummy_atoms():
    atoms = [Atom(symbol='DA', x=0.0, y=0.0, z=0.0)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nDA 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()
