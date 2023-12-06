import pytest
from pychum.engine.orca._dataclasses import GeomScan, OrcaGeom
from pychum.engine.orca._renderer import OrcaInputRenderer

# Helper function to render the geometry scan block
def render_geom_scan(orca_geom):
    config = {'orca_geom': orca_geom}
    renderer = OrcaInputRenderer(config)
    return renderer.render('geom_scan.jinja')

# Test cases
def test_single_bond_scan():
    geom = OrcaGeom(bonds=[GeomScan(atoms=[0, 1], range=[1.0, 2.0], points=10)])
    result = render_geom_scan(geom)
    expected = "%geom\n Scan\n    B 0 1 = 1.0, 2.0, 10\n end\nend"
    assert result.strip() == expected

def test_single_angle_scan():
    geom = OrcaGeom(angles=[GeomScan(atoms=[0, 1, 2], range=[90, 180], points=5)])
    result = render_geom_scan(geom)
    expected = "%geom\n Scan\n    A 0 1 2 = 90, 180, 5\n end\nend"
    assert result.strip() == expected

def test_single_dihedral_scan():
    geom = OrcaGeom(dihedrals=[GeomScan(atoms=[0, 1, 2, 3], range=[0, 360], points=20)])
    result = render_geom_scan(geom)
    expected = "%geom\n Scan\n    D 0 1 2 3 = 0, 360, 20\n end\nend"
    assert result.strip() == expected

def test_combined_scans():
    geom = OrcaGeom(
        bonds=[GeomScan(atoms=[0, 1], range=[1.0, 2.0], points=10)],
        angles=[GeomScan(atoms=[0, 1, 2], range=[90, 180], points=5)],
        dihedrals=[GeomScan(atoms=[0, 1, 2, 3], range=[0, 360], points=20)]
    )
    result = render_geom_scan(geom)
    # TODO(rg): Maybe fix the spacing here?
    expected = (
        "%geom\n"
        " Scan\n"
        "    B 0 1 = 1.0, 2.0, 10\n\n"
        "    A 0 1 2 = 90, 180, 5\n\n"
        "    D 0 1 2 3 = 0, 360, 20\n"
        " end\n"
        "end"
    )
    assert result.strip() == expected

def test_exceeding_scan_limit():
    geom = OrcaGeom(
        bonds=[GeomScan(atoms=[0, 1], range=[1.0, 2.0], points=10)] * 4
    )
    result = render_geom_scan(geom)
    expected = "Error: More than three scan coordinates are defined."
    assert expected in result.strip()
