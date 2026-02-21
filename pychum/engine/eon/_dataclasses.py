from dataclasses import dataclass
from pathlib import Path


@dataclass
class NWChemAtom:
    symbol: str
    x: float
    y: float
    z: float


@dataclass
class NWChemSocketConfig:
    atoms: list[NWChemAtom]
    settings_path: Path
    socket_address: str
    unix_mode: bool = False
    mem_in_gb: int = 2
    output_path: Path = Path("nwchem_socket.nwi")
