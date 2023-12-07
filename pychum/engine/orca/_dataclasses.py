from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class UnitConversion:
    inp: str
    out: str

@dataclass
class Atom:
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    symbol: str = field(default=None)
    is_ghost: bool = False
    embedding_potential: bool = False
    is_frozen: bool = False # Not applied to anything but cartesian
    isotope: Optional[float] = None
    nuclear_charge: Optional[float] = None
    fragment_number: Optional[int] = None
    is_dummy: bool = False
    point_charge: Optional[float] = None
    bond_atom: Optional[int] = None  # Index of bonded atom (for internal coordinates)
    bond_length: Optional[float] = None  # Bond length (for internal coordinates)
    angle_atom: Optional[int] = None  # Index of angle atom (for internal coordinates)
    angle: Optional[float] = None  # Bond angle (for internal coordinates)
    dihedral_atom: Optional[int] = None  # Index of dihedral atom (for internal coordinates)
    dihedral: Optional[float] = None  # Dihedral angle (for internal coordinates)
    is_frozen_x: bool = False # Cartesian only
    is_frozen_y: bool = False # Cartesian only
    is_frozen_z: bool = False # Cartesian only

    def __post_init__(self):
        if self.point_charge is not None:
            self.symbol = 'Q'
        elif self.symbol is None:
            raise ValueError("Atom symbol is required unless it's a point charge.")

@dataclass
class Coords:
    charge: int
    multiplicity: int
    fmt: str
    filedat: str = ""
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
    # units_distance: Optional[List[UnitConversion]]
    # units_energy: List[UnitConversion]
    coords: Coords
    orca_geom: Optional[OrcaGeom] = None
