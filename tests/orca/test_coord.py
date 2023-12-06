import textwrap
from pychum.engine.orca._dataclasses import Atom, OrcaConfig, Coords
from pychum.engine.orca._renderer import OrcaInputRenderer

def render_config(atoms, coord_type='xyz', charge=0, multiplicity=1):
    coords = Coords(charge=charge, multiplicity=multiplicity, atoms=atoms, fmt = coord_type)
    config = OrcaConfig(coords=coords)
    renderer = OrcaInputRenderer(config)
    return renderer.render('coord.jinja')

def test_standard_atoms_xyz():
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0), Atom(symbol='O', x=0.0, y=0.0, z=1.13)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.0 0.0 0.0\nO 0.0 0.0 1.13\n*"
    assert result.strip() == expected.strip()

def test_dummy_atoms():
    atoms = [Atom(symbol='DA', x=0.0, y=0.0, z=0.0)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nDA 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()

def test_ghost_atoms():
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0, is_ghost=True)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC: 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()

def test_point_charges():
    atoms = [Atom(point_charge=-0.834, x=-1.3130, y= 0.0, z=0.0898)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nQ -0.834 -1.313 0.0 0.0898\n*"
    assert result.strip() == expected.strip()

def test_atoms_with_isotopes():
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0, isotope=13)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.0 0.0 0.0 M = 13\n*"
    assert result.strip() == expected.strip()

def test_frozen_coordinates():
    # Test with all coordinates frozen
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0, is_frozen_x=True, is_frozen_y=True, is_frozen_z=True)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.0$ 0.0$ 0.0$\n*"
    assert result.strip() == expected.strip()

    # Test with individual coordinates frozen
    atoms = [Atom(symbol='C', x=0.2, y=0.3, z=0.6, is_frozen_x=True, is_frozen_y=False, is_frozen_z=True)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.2$ 0.3 0.6$\n*"
    assert result.strip() == expected.strip()

    # Test with no coordinates frozen
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0, is_frozen_x=False, is_frozen_y=False, is_frozen_z=False)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()

def test_embedding_potentials():
    atoms = [Atom(symbol='C', x=0.0, y=0.0, z=0.0, embedding_potential=True)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nC > 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()

def test_nuclear_charges():
    atoms = [Atom(symbol='O', x=0.0, y=0.0, z=0.0, nuclear_charge=8.5)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nO 0.0 0.0 0.0 Z = 8.5\n*"
    assert result.strip() == expected.strip()

def test_fragments():
    atoms = [Atom(symbol='H', x=0.0, y=0.0, z=0.0, fragment_number=1)]
    result = render_config(atoms)
    expected = "* xyz 0 1\nH (1) 0.0 0.0 0.0\n*"
    assert result.strip() == expected.strip()

def test_internal_coordinates():
    atoms = [
        Atom(symbol='C', bond_atom=0, bond_length=0.0, angle_atom=0, angle=0.0, dihedral_atom=0, dihedral=0.0),
        Atom(symbol='O', bond_atom=1, bond_length=1.3500, angle_atom=0, angle=0.0, dihedral_atom=0, dihedral=0.0),
        Atom(symbol='H', bond_atom=1, bond_length=1.1075, angle_atom=2, angle=122.016, dihedral_atom=0, dihedral=0.0),
        Atom(symbol='H', bond_atom=1, bond_length=1.1075, angle_atom=2, angle=122.016, dihedral_atom=3, dihedral=180.0)
    ]
    result = render_config(atoms, coord_type='int')
    expected = """
    * int 0 1
    C 0 0 0 0.0 0.0 0.0
    O 1 0 0 1.35 0.0 0.0
    H 1 2 0 1.1075 122.016 0.0
    H 1 2 3 1.1075 122.016 180.0
    *
    """
    assert result.strip() == textwrap.dedent(expected).strip()

def test_gaussian_z_matrix():
    atoms = [
        Atom(symbol='O'),
        Atom(symbol='C', bond_atom=1, bond_length=1.2078),
        Atom(symbol='H', bond_atom=2, bond_length=1.1161, angle_atom=1, angle=121.74),
        Atom(symbol='H', bond_atom=2, bond_length=1.1161, angle_atom=1, angle=121.74, dihedral_atom=3, dihedral=180)
    ]
    result = render_config(atoms, coord_type='gzmt')
    expected = """
    * gzmt 0 1
    O
    C 1 1.2078
    H 2 1.1161 1 121.74
    H 2 1.1161 1 121.74 3 180
    *
    """
    assert result.strip() == textwrap.dedent(expected).strip()
