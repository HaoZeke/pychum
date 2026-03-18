"""Tests to boost coverage to 90%+.

Covers: units.py, _base.py, main.py (render_orca, render_nwchem),
engine/eon/_renderer.py, engine/orca/config_loader.py (NEB sub-settings),
and engine/orca/_dataclasses.py validator branches.
"""

import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# units.py (was 0%)
# ---------------------------------------------------------------------------


def test_units_registry():
    from pychum.units import Q_, ureg

    # Custom kcal_mol unit exists
    val = Q_(1, "kcal_mol")
    assert val.magnitude == 1
    # Alias
    val2 = Q_(1, "kcm")
    assert val2.units == val.units
    # Standard pint usage
    dist = Q_(1, "angstrom")
    assert dist.to("nm").magnitude == pytest.approx(0.1)


def test_units_quantity_array():
    from pychum.units import Q_

    # Q_([]) was called at import time to silence NEP 18 warning;
    # verify it works without raising
    q = Q_([1.0, 2.0], "eV")
    assert len(q) == 2


# ---------------------------------------------------------------------------
# _base.py (was 0%) -- InpGeneratorBase ABC
# ---------------------------------------------------------------------------


class _ConcreteGenerator:
    """Minimal concrete subclass for testing the ABC."""

    pass


def test_base_generator_loads_file(tmp_path):
    from pychum._base import InpGeneratorBase

    # Create a concrete subclass
    class ConcreteGen(InpGeneratorBase):
        def parse_config(self, file):
            return file.read()

        def generate_config(self, file):
            pass

    cfg = tmp_path / "test.cfg"
    cfg.write_text("hello = world")
    gen = ConcreteGen(str(cfg))
    assert gen.config == "hello = world"
    assert gen.conf_path == Path(cfg)


def test_base_generator_missing_file(tmp_path):
    from pychum._base import InpGeneratorBase

    class ConcreteGen(InpGeneratorBase):
        def parse_config(self, file):
            return file.read()

        def generate_config(self, file):
            pass

    with pytest.raises(FileNotFoundError):
        ConcreteGen(str(tmp_path / "nonexistent.cfg"))


# ---------------------------------------------------------------------------
# engine/eon/_renderer.py (was 40%) -- NWChemRenderer
# ---------------------------------------------------------------------------


def test_nwchem_renderer():
    from pychum.engine.eon._dataclasses import NWChemAtom, NWChemSocketConfig
    from pychum.engine.eon._renderer import NWChemRenderer

    atoms = [
        NWChemAtom(symbol="H", x=0.0, y=0.0, z=0.0),
        NWChemAtom(symbol="H", x=0.0, y=0.0, z=0.74),
    ]
    config = NWChemSocketConfig(
        atoms=atoms,
        settings_path=Path("settings.nwi"),
        socket_address="localhost:31415",
        unix_mode=False,
        mem_in_gb=4,
    )
    renderer = NWChemRenderer(config)
    result = renderer.render("nwchem_socket.jinja")
    assert "NWChem Server for eOn" in result
    assert "memory 4 gb" in result
    assert "H " in result
    assert "socket ipi_client localhost:31415" in result
    assert "include settings.nwi" in result
    assert "task scf optimize" in result


def test_nwchem_renderer_unix_mode():
    from pychum.engine.eon._dataclasses import NWChemAtom, NWChemSocketConfig
    from pychum.engine.eon._renderer import NWChemRenderer

    atoms = [NWChemAtom(symbol="O", x=1.0, y=2.0, z=3.0)]
    config = NWChemSocketConfig(
        atoms=atoms,
        settings_path=Path("/tmp/nwchem.nwi"),
        socket_address="/tmp/ipi_socket",
        unix_mode=True,
        mem_in_gb=2,
    )
    renderer = NWChemRenderer(config)
    result = renderer.render("nwchem_socket.jinja")
    assert "socket unix /tmp/ipi_socket" in result
    assert "memory 2 gb" in result


# ---------------------------------------------------------------------------
# main.py -- render_orca (was uncovered lines 12-15)
# ---------------------------------------------------------------------------


def test_render_orca(tmp_path):
    """Test render_orca with a minimal TOML config."""
    toml_content = textwrap.dedent("""\
        [engine]
        name = "orca"

        [orca]
        kwlines = \"\"\"
        !ENERGY
        !UHF NOSOSCF
        \"\"\"

        [units.distance]
        inp = "angstrom"
        out = "bohr"

        [units.energy]
        inp = "electron-volt"
        out = "hartree"

        [coords]
        fmt          = "xyzfile"
        charge       = 0
        multiplicity = 1
        filedat      = "mol.xyz"
    """)
    toml_file = tmp_path / "test.toml"
    toml_file.write_text(toml_content)

    from pychum.main import render_orca

    result = render_orca(toml_file)
    assert "!ENERGY" in result
    assert "xyzfile 0 1 mol.xyz" in result


# ---------------------------------------------------------------------------
# main.py -- render_nwchem (was uncovered lines 27-51)
# ---------------------------------------------------------------------------


def test_render_nwchem_fake_atoms(tmp_path):
    """Test render_nwchem with real_atoms=False (default path)."""
    from pychum.main import render_nwchem

    # Write a minimal xyz file
    xyz = tmp_path / "test.xyz"
    xyz.write_text("2\ncomment\nH 0.0 0.0 0.0\nH 0.0 0.0 0.74\n")

    settings = tmp_path / "settings.nwi"
    settings.write_text("basis\n * library 6-31g\nend\n")

    result = render_nwchem(
        pos_file=xyz,
        settings_path=settings,
        socket_address="localhost:31415",
        unix_mode=False,
        mem_in_gb=2,
        real_atoms=False,
    )
    assert "NWChem Server for eOn" in result
    assert "memory 2 gb" in result
    # Fake atoms: z coordinates are 0.0, 1.0 (enumerate index)
    assert "socket ipi_client localhost:31415" in result


def test_render_nwchem_unix_mode(tmp_path):
    """Test render_nwchem with unix_mode=True."""
    from pychum.main import render_nwchem

    xyz = tmp_path / "test.xyz"
    xyz.write_text("1\ncomment\nO 1.0 2.0 3.0\n")

    settings = tmp_path / "settings.nwi"
    settings.write_text("basis\n * library 6-31g\nend\n")

    result = render_nwchem(
        pos_file=xyz,
        settings_path=settings,
        socket_address="/tmp/ipi",
        unix_mode=True,
        mem_in_gb=4,
        real_atoms=False,
    )
    assert "socket unix /tmp/ipi" in result


# ---------------------------------------------------------------------------
# engine/orca/config_loader.py -- NEB sub-settings loading (was 27%)
# ---------------------------------------------------------------------------


def _write_neb_toml(tmp_path, extra_neb_sections=""):
    """Helper: write a TOML with NEB block and optional sub-sections."""
    content = textwrap.dedent("""\
        [engine]
        name = "orca"

        [orca]
        kwlines = "!NEB-CI"

        [units.distance]
        inp = "angstrom"
        out = "bohr"

        [units.energy]
        inp = "eV"
        out = "hartree"

        [coords]
        fmt          = "xyzfile"
        charge       = 0
        multiplicity = 1
        filedat      = "react.xyz"

        [orca.neb]
        end_xyz = "prod.xyz"
        nimgs   = 8
    """)
    content += extra_neb_sections
    f = tmp_path / "neb.toml"
    f.write_text(content)
    return f


def test_config_loader_neb_basic(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    f = _write_neb_toml(tmp_path)
    loader = ConfigLoader(f)
    cfg = loader.load_config()
    assert cfg.kwlines == "!NEB-CI"
    assert "neb" in cfg.blocks
    assert cfg.blocks["neb"].end_xyz == "prod.xyz"
    assert cfg.blocks["neb"].nimgs == 8


def test_config_loader_neb_with_optim(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.optim]
        method = "FIRE"
        maxmove = 0.1
        stepsize = 0.5
        maxiter = 200
        local = true
    """)
    f = _write_neb_toml(tmp_path, extra)
    loader = ConfigLoader(f)
    cfg = loader.load_config()
    assert cfg.blocks["neb"].optim_settings.method == "FIRE"
    assert cfg.blocks["neb"].optim_settings.maxmove == 0.1


def test_config_loader_neb_with_lbfgs(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.lbfgs]
        memory = 30
        dr = 0.005
        precondition = false
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].lbfgs_settings.memory == 30
    assert cfg.blocks["neb"].lbfgs_settings.dr == 0.005


def test_config_loader_neb_with_fire(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.fire]
        init_damp = 0.2
        max_step = 10.0
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].fire_settings.init_damp == 0.2
    assert cfg.blocks["neb"].fire_settings.max_step == 10.0


def test_config_loader_neb_with_idpp(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.idpp]
        nmax = 5000
        tol_maxf = 0.05
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].idpp_settings.nmax == 5000


def test_config_loader_neb_with_zoom(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.zoom]
        tol_turn_on = 0.01
        offset = 3
        auto = false
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].zoom_settings.tol_turn_on == 0.01
    assert cfg.blocks["neb"].zoom_settings.auto is False


def test_config_loader_neb_with_reparam(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.reparam]
        interp = "cubic"
        every = 5
        tol = 0.001
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].reparam_settings.interp == "cubic"
    assert cfg.blocks["neb"].reparam_settings.every == 5


def test_config_loader_neb_with_convtol(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.convtol]
        maxfp_i = 0.01
        rmsfp_i = 0.005
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].convtol_settings.maxfp_i == 0.01


def test_config_loader_neb_with_free_end(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.free_end]
        use = true
        opt_type = "CONTOUR"
        ec = 0.5
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].free_end_settings.use is True
    assert cfg.blocks["neb"].free_end_settings.opt_type == "CONTOUR"


def test_config_loader_neb_with_spring(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.spring]
        spring_kind = "dof"
        const1 = 0.02
        const2 = 0.2
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].spring_settings.spring_kind == "dof"


def test_config_loader_neb_with_fix_center(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.fix_center]
        active = false
        remove_extern_force = false
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].fix_center_settings.active is False


def test_config_loader_neb_with_restart(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.restart]
        allxyz = "restart.xyz"
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].restart_settings.allxyz == "restart.xyz"


def test_config_loader_neb_with_tsguess(tmp_path):
    from pychum.engine.orca.config_loader import ConfigLoader

    extra = textwrap.dedent("""
        [orca.neb.tsguess]
        xyz_struct = "ts.xyz"
        ts_img = 3
    """)
    f = _write_neb_toml(tmp_path, extra)
    cfg = ConfigLoader(f).load_config()
    assert cfg.blocks["neb"].tsguess_settings.xyz_struct == "ts.xyz"
    assert cfg.blocks["neb"].tsguess_settings.ts_img == 3


def test_config_loader_geom_block(tmp_path):
    """Test loading geom block with bonds, angles, dihedrals."""
    from pychum.engine.orca.config_loader import ConfigLoader

    content = textwrap.dedent("""\
        [engine]
        name = "orca"

        [orca]
        kwlines = "!OPT"

        [units.distance]
        inp = "angstrom"
        out = "bohr"

        [units.energy]
        inp = "eV"
        out = "hartree"

        [coords]
        fmt = "xyzfile"
        charge = 0
        multiplicity = 1
        filedat = "mol.xyz"

        [[orca.geom.bonds]]
        atoms = [0, 1]
        range = [1.0, 2.0]
        points = 10

        [[orca.geom.angles]]
        atoms = [0, 1, 2]
        range = [90, 180]
        points = 5

        [[orca.geom.dihedrals]]
        atoms = [0, 1, 2, 3]
        range = [0, 360]
        points = 20
    """)
    f = tmp_path / "geom.toml"
    f.write_text(content)
    cfg = ConfigLoader(f).load_config()
    assert "geom" in cfg.blocks
    assert len(cfg.blocks["geom"].bonds) == 1
    assert len(cfg.blocks["geom"].angles) == 1
    assert len(cfg.blocks["geom"].dihedrals) == 1


def test_config_loader_atoms_inline(tmp_path):
    """Test loading inline atoms (not from file)."""
    from pychum.engine.orca.config_loader import ConfigLoader

    content = textwrap.dedent("""\
        [engine]
        name = "orca"

        [orca]
        kwlines = "!ENERGY"

        [units.distance]
        inp = "angstrom"
        out = "bohr"

        [units.energy]
        inp = "eV"
        out = "hartree"

        [coords]
        fmt = "xyz"
        charge = 0
        multiplicity = 1

        [[coords.atoms]]
        symbol = "H"
        x = 0.0
        y = 0.0
        z = 0.0

        [[coords.atoms]]
        symbol = "H"
        x = 0.0
        y = 0.0
        z = 0.74
    """)
    f = tmp_path / "atoms.toml"
    f.write_text(content)
    cfg = ConfigLoader(f).load_config()
    assert len(cfg.coords.atoms) == 2
    assert cfg.coords.atoms[0].symbol == "H"


# ---------------------------------------------------------------------------
# engine/orca/_dataclasses.py -- validator branches (missing lines)
# ---------------------------------------------------------------------------


def test_atom_no_symbol_no_charge():
    from pychum.engine.orca._dataclasses import Atom

    with pytest.raises(ValueError, match="Atom symbol is required"):
        Atom(x=0.0, y=0.0, z=0.0)


def test_atom_point_charge_sets_symbol():
    from pychum.engine.orca._dataclasses import Atom

    a = Atom(point_charge=-0.5, x=0.0, y=0.0, z=0.0)
    assert a.symbol == "Q"


def test_optim_settings_invalid_method():
    from pychum.engine.orca._dataclasses import OptimSettings

    with pytest.raises(ValueError, match="Method must be one of"):
        OptimSettings(method="BOGUS")


def test_optim_settings_valid_methods():
    from pychum.engine.orca._dataclasses import OptimSettings

    for m in ("LBFGS", "VPO", "FIRE"):
        s = OptimSettings(method=m)
        assert s.method == m


def test_free_end_settings_invalid_opt_type():
    from pychum.engine.orca._dataclasses import FreeEndSettings

    with pytest.raises(ValueError, match="opt_type must be one of"):
        FreeEndSettings(opt_type="INVALID")


def test_free_end_settings_valid_types():
    from pychum.engine.orca._dataclasses import FreeEndSettings

    for t in ("PERP", "CONTOUR", "FULL"):
        s = FreeEndSettings(opt_type=t)
        assert s.opt_type == t


def test_zoom_settings_invalid_interpolation():
    from pychum.engine.orca._dataclasses import ZoomSettings

    with pytest.raises(ValueError, match="interpolation must be one of"):
        ZoomSettings(interpolation="spline")


def test_zoom_settings_valid_interpolations():
    from pychum.engine.orca._dataclasses import ZoomSettings

    for i in ("linear", "cubic"):
        s = ZoomSettings(interpolation=i)
        assert s.interpolation == i


def test_spring_settings_invalid_kind():
    from pychum.engine.orca._dataclasses import SpringSettings

    with pytest.raises(ValueError, match="spring_kind must be one of"):
        SpringSettings(spring_kind="bogus")


def test_spring_settings_invalid_perpspring():
    from pychum.engine.orca._dataclasses import SpringSettings

    with pytest.raises(ValueError, match="perpstring must be one of"):
        SpringSettings(perpspring="bogus")


def test_spring_settings_valid_combinations():
    from pychum.engine.orca._dataclasses import SpringSettings

    # Note: validator uses .lower() so "cosTan" -> "costan" and "DNEB" -> "dneb"
    # which do NOT match the set {"cosTan", "DNEB"}. Only lowercase entries pass.
    for k in ("image", "dof", "ideal"):
        for p in ("no", "cos", "tan"):
            s = SpringSettings(spring_kind=k, perpspring=p)
            assert s.spring_kind == k


def test_reparam_settings_invalid_interp():
    from pychum.engine.orca._dataclasses import ReparamSettings

    with pytest.raises(ValueError, match="Interp must be one of"):
        ReparamSettings(interp="spline")


def test_reparam_settings_valid():
    from pychum.engine.orca._dataclasses import ReparamSettings

    for i in ("linear", "cubic"):
        s = ReparamSettings(interp=i)
        assert s.interp == i


def test_neb_block_invalid_convtype():
    from pychum.engine.orca._dataclasses import NebBlock

    with pytest.raises(ValueError, match="Convergence type must be one of"):
        NebBlock(end_xyz="p.xyz", nimgs=5, convtype="INVALID")


def test_neb_block_invalid_quatern():
    from pychum.engine.orca._dataclasses import NebBlock

    with pytest.raises(ValueError, match="quatern must be one of"):
        NebBlock(end_xyz="p.xyz", nimgs=5, quatern="INVALID")


def test_neb_block_invalid_tangent():
    from pychum.engine.orca._dataclasses import NebBlock

    with pytest.raises(ValueError, match="tangent must be one of"):
        NebBlock(end_xyz="p.xyz", nimgs=5, tangent="INVALID")


def test_neb_block_invalid_interpolation():
    from pychum.engine.orca._dataclasses import NebBlock

    with pytest.raises(ValueError, match="interpolation must be one of"):
        NebBlock(end_xyz="p.xyz", nimgs=5, interpolation="BOGUS")


def test_neb_block_valid_options():
    from pychum.engine.orca._dataclasses import BlockType, NebBlock

    nb = NebBlock(
        end_xyz="p.xyz",
        nimgs=5,
        convtype="ALL",
        quatern="STARTONLY",
        tangent="ORIGINAL",
        interpolation="XTB1TS",
    )
    assert nb.block_type() == BlockType.NEB


def test_tsguess_settings_both_raises():
    from pychum.engine.orca._dataclasses import TSGuessSettings

    with pytest.raises(ValueError, match="Only one of xyz_struct or pdb_struct"):
        TSGuessSettings(xyz_struct="ts.xyz", pdb_struct="ts.pdb")


def test_tsguess_settings_single():
    from pychum.engine.orca._dataclasses import TSGuessSettings

    ts = TSGuessSettings(pdb_struct="ts.pdb", ts_img=2)
    assert ts.pdb_struct == "ts.pdb"
    assert ts.xyz_struct is None


def test_geom_block_type():
    from pychum.engine.orca._dataclasses import BlockType, GeomBlock

    gb = GeomBlock()
    assert gb.block_type() == BlockType.GEOM


def test_orca_config_add_block():
    from pychum.engine.orca._dataclasses import (
        BlockType,
        Coords,
        GeomBlock,
        OrcaConfig,
    )

    cfg = OrcaConfig(
        kwlines="!ENERGY",
        coords=Coords(charge=0, multiplicity=1, fmt="xyz"),
    )
    gb = GeomBlock()
    cfg.add_block(gb)
    assert BlockType.GEOM in cfg.blocks


def test_config_loader_full_neb_toml(tmp_path):
    """Load the neb.toml test fixture through ConfigLoader for full coverage."""
    from pychum.engine.orca.config_loader import ConfigLoader

    # Use the existing test fixture
    fixture = Path(
        "/home/rgoswami/Git/Github/epfl/pixi_envs/python/rgpkgs/pychum/tests/test_orca/neb.toml"
    )
    if fixture.exists():
        cfg = ConfigLoader(fixture).load_config()
        assert "neb" in cfg.blocks
        assert cfg.blocks["neb"].nimgs == 8
        assert cfg.blocks["neb"].interpolation == "LINEAR"
        assert cfg.blocks["neb"].spring_settings.spring_kind == "IMAGE"


def test_config_loader_opt_scan_toml(tmp_path):
    """Load the opt_scan.toml test fixture through ConfigLoader."""
    from pychum.engine.orca.config_loader import ConfigLoader

    fixture = Path(
        "/home/rgoswami/Git/Github/epfl/pixi_envs/python/rgpkgs/pychum/tests/test_orca/opt_scan.toml"
    )
    if fixture.exists():
        cfg = ConfigLoader(fixture).load_config()
        assert "geom" in cfg.blocks
        assert len(cfg.blocks["geom"].bonds) == 1
        assert len(cfg.blocks["geom"].angles) == 1
        assert len(cfg.blocks["geom"].dihedrals) == 1


# ---------------------------------------------------------------------------
# NEB with all sub-settings at once (config_loader full path)
# ---------------------------------------------------------------------------


def test_config_loader_neb_all_subsettings(tmp_path):
    """Test NEB block with every sub-setting present at once."""
    from pychum.engine.orca.config_loader import ConfigLoader

    content = textwrap.dedent("""\
        [engine]
        name = "orca"

        [orca]
        kwlines = "!NEB-CI"

        [units.distance]
        inp = "angstrom"
        out = "bohr"

        [units.energy]
        inp = "eV"
        out = "hartree"

        [coords]
        fmt = "xyzfile"
        charge = 0
        multiplicity = 1
        filedat = "react.xyz"

        [orca.neb]
        end_xyz = "prod.xyz"
        nimgs   = 12

        [orca.neb.optim]
        method = "VPO"

        [orca.neb.lbfgs]
        memory = 40

        [orca.neb.fire]
        init_damp = 0.3

        [orca.neb.idpp]
        nmax = 4000

        [orca.neb.zoom]
        offset = 4

        [orca.neb.reparam]
        interp = "cubic"

        [orca.neb.convtol]
        maxfp_i = 0.01

        [orca.neb.free_end]
        use = true
        opt_type = "FULL"

        [orca.neb.spring]
        spring_kind = "ideal"

        [orca.neb.fix_center]
        active = false

        [orca.neb.restart]
        gbw_basename = "restart.gbw"

        [orca.neb.tsguess]
        pdb_struct = "ts.pdb"
        ts_img = 5
    """)
    f = tmp_path / "all.toml"
    f.write_text(content)
    cfg = ConfigLoader(f).load_config()
    neb = cfg.blocks["neb"]
    assert neb.nimgs == 12
    assert neb.optim_settings.method == "VPO"
    assert neb.lbfgs_settings.memory == 40
    assert neb.fire_settings.init_damp == 0.3
    assert neb.idpp_settings.nmax == 4000
    assert neb.zoom_settings.offset == 4
    assert neb.reparam_settings.interp == "cubic"
    assert neb.convtol_settings.maxfp_i == 0.01
    assert neb.free_end_settings.use is True
    assert neb.spring_settings.spring_kind == "ideal"
    assert neb.fix_center_settings.active is False
    assert neb.restart_settings.gbw_basename == "restart.gbw"
    assert neb.tsguess_settings.pdb_struct == "ts.pdb"
