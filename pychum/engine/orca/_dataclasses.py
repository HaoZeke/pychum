from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class UnitConversion:
    inp: str
    out: str

@dataclass
class Atom:
    symbol: str
    x: float
    y: float
    z: float
    is_ghost: bool = False
    embedding_potential: bool = False
    is_frozen: bool = False
    isotope: Optional[float] = None  # Isotope mass number
    nuclear_charge: Optional[float] = None  # Non-standard nuclear charge
    fragment_number: Optional[int] = None  # Fragment number
    is_dummy: bool = False  # Indicates if the atom is a dummy atom
    point_charge: Optional[float] = None  # Value of the point charge


@dataclass
class FileData:
    source: str
    fname: str

@dataclass
class Coords:
    charge: int
    multiplicity: int
    fmt: str
    filedat: List[FileData] = field(default_factory=list)
    atoms: List[Atom] = field(default_factory=list)

@dataclass
class GeomScan:
    atoms: List[int]
    range: List[float]
    points: int

@dataclass
class OrcaGeom:
    bonds: List[GeomScan] = field(default_factory=list)
    dihedrals: List[GeomScan] = field(default_factory=list)
    angles: List[GeomScan] = field(default_factory=list)

@dataclass
class OrcaConfig:
    engine: str
    # units_distance: Optional[List[UnitConversion]]
    # units_energy: List[UnitConversion]
    coords: Coords
    # orca_geom: OrcaGeom
