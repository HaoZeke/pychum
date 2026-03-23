from pathlib import Path

from ase.io import read as ase_read

from pychum.engine.eon import NWChemAtom, NWChemRenderer, NWChemSocketConfig
from pychum.engine.orca._renderer import OrcaInputRenderer
from pychum.engine.orca.config_loader import ConfigLoader


def render_orca(toml_path: Path) -> str:
    """Library function to render ORCA input from a TOML file."""
    config_loader = ConfigLoader(toml_path)
    config = config_loader.load_config()
    renderer = OrcaInputRenderer(config)
    return renderer.render("base.jinja")


def render_nwchem(
    pos_file: Path,
    settings_path: Path,
    socket_address: str,
    unix_mode: bool,  # noqa: FBT001
    mem_in_gb: int,
    real_atoms: bool = False,  # noqa: FBT001, FBT002
) -> str:
    """Library function to render NWChem input."""
    atoms = ase_read(pos_file)
    if real_atoms:
        nw_atoms = [
            NWChemAtom(symbol=atom.symbol, x=atom.x, y=atom.y, z=atom.z) for atom in atoms
        ]
    else:
        nw_atoms = [
            # This is intentionally broken, in that the positions are
            # overwritten by eOn on first run anyway, so we just need them to
            # not overlap
            NWChemAtom(symbol=atom.symbol, x=0.0, y=0.0, z=float(i))
            for i, atom in enumerate(atoms)
        ]

    nw_config = NWChemSocketConfig(
        atoms=nw_atoms,
        settings_path=settings_path,
        socket_address=socket_address,
        unix_mode=unix_mode,
        mem_in_gb=mem_in_gb,
    )

    renderer = NWChemRenderer(nw_config)
    return renderer.render("nwchem_socket.jinja")
