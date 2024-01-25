from dataclasses import dataclass, field
from typing import List, Optional, Dict
from abc import ABC, abstractmethod
from enum import Enum


class BlockType(Enum):
    NEB = "neb"
    SCF = "scf"
    GEOM = "geom"


class OrcaBlock(ABC):
    @abstractmethod
    def block_type(self) -> BlockType:
        pass


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
    is_frozen: bool = False  # Not applied to anything but cartesian
    isotope: Optional[float] = None
    nuclear_charge: Optional[float] = None
    fragment_number: Optional[int] = None
    is_dummy: bool = False
    point_charge: Optional[float] = None
    bond_atom: Optional[int] = None  # Index of bonded atom (for internal coordinates)
    bond_length: Optional[float] = None  # Bond length (for internal coordinates)
    angle_atom: Optional[int] = None  # Index of angle atom (for internal coordinates)
    angle: Optional[float] = None  # Bond angle (for internal coordinates)
    dihedral_atom: Optional[
        int
    ] = None  # Index of dihedral atom (for internal coordinates)
    dihedral: Optional[float] = None  # Dihedral angle (for internal coordinates)
    is_frozen_x: bool = False  # Cartesian only
    is_frozen_y: bool = False  # Cartesian only
    is_frozen_z: bool = False  # Cartesian only

    def __post_init__(self):
        if self.point_charge is not None:
            self.symbol = "Q"
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
class GeomBlock(OrcaBlock):
    bonds: List[GeomScan] = field(default_factory=list)
    dihedrals: List[GeomScan] = field(default_factory=list)
    angles: List[GeomScan] = field(default_factory=list)

    def block_type(self) -> BlockType:
        return BlockType.GEOM


@dataclass
class LBFGSSettings:
    reparam_on_restart: bool = False
    memory: int = 20
    precondition: bool = True
    dr: float = 0.002
    restart_on_maxmove: bool = True


@dataclass
class FIRESettings:
    init_damp: float = 0.1
    damp_decr: float = 0.99
    step_incr: float = 1.1
    step_decr: float = 0.5
    max_step: float = 5.0
    retention: int = 5


@dataclass
class ReparamSettings:
    interp: str = "linear"
    every: int = 0
    tol: float = 0.0

    def __post_init__(self):
        valid_interps = {"linear", "cubic"}
        if self.interp.lower() not in valid_interps:
            raise ValueError(
                f"Interp must be one of {valid_interps}, got '{self.interp}'"
            )


@dataclass
class ConvTolSettings:
    units: str = "Eh/Bohr"
    maxfp_i: float = 0.005
    rmsfp_i: float = 0.003
    maxf_ci: float = 0.0005
    rmsf_ci: float = 0.0003
    turn_on_ci: float = 0.02
    scale: int = 10


@dataclass
class IDPPSettings:
    tol_maxf: float = 0.01
    maxmove: float = 0.05
    alpha: float = 0.01
    nmax: int = 3000
    quatern: bool = True
    ksp: float = 1.0
    debug: bool = False


@dataclass
class OptimSettings:
    method: str = "LBFGS"
    maxmove: float = 0.2
    stepsize: float = 1.0
    maxiter: float = 500
    local: bool = False

    def __post_init__(self):
        valid_methods = {"LBFGS", "VPO", "FIRE"}
        if self.method.upper() not in valid_methods:
            raise ValueError(
                f"Method must be one of {valid_methods}, got '{self.method}'"
            )


@dataclass
class ZoomSettings:
    tol_turn_on: float = 0.0
    offset: int = 2
    auto: bool = True
    tol_scale: int = 10
    alpha: float = 0.5
    printfulltrj: bool = True


@dataclass
class NebBlock(OrcaBlock):
    end_xyz: str
    nimgs: int
    free_end_kappa: float = 1.0
    free_end: bool = False
    springtype: str = "IMAGE"
    springconst: float = 0.01
    free_end_type: str = "PERP"
    reparam: int = 0
    free_end_ec: float = 0.0
    springconst2: float = 0.1
    convtype: str = "CIONLY"
    tangent: str = "IMPROVED"
    printlevel: int = 4
    neb_ts: bool = False
    quatern: str = "ALWAYS"
    interpolation: str = "IDPP"
    climbingimage: bool = True
    restart_opt_on_reparam: bool = False
    free_end_ec_end: float = 0.0
    energy_weighted: bool = True
    perpspring: str = "NO"
    maxiter: int = 500
    remove_extern_force: bool = True
    local: bool = False
    fix_center: bool = True

    lbfgs_settings: LBFGSSettings = field(default_factory=LBFGSSettings)
    fire_settings: FIRESettings = field(default_factory=FIRESettings)
    reparam_settings: ReparamSettings = field(default_factory=ReparamSettings)
    idpp_settings: IDPPSettings = field(default_factory=IDPPSettings)
    zoom_settings: ZoomSettings = field(default_factory=ZoomSettings)
    optim_settings: OptimSettings = field(default_factory=OptimSettings)
    convtol_settings: ConvTolSettings = field(default_factory=ConvTolSettings)

    def __post_init__(self):
        valid_convtypes = {"all", "cionly"}
        if self.convtype.lower() not in valid_convtypes:
            raise ValueError(
                f"Convergence type must be one of {valid_convtypes}, got '{self.convtype}'"
            )

    def block_type(self) -> BlockType:
        return BlockType.NEB


@dataclass
class KWLine:
    runtype: str = "!ENERGY"
    safeopts: str = "!UHF NOSOSCF ForceConv"
    extra: str = None


@dataclass
class OrcaConfig:
    coords: Coords
    kwlines: List[KWLine] = field(default_factory=list)
    blocks: Dict[BlockType, OrcaBlock] = field(default_factory=dict)

    def add_block(self, block: OrcaBlock):
        self.blocks[block.block_type()] = block


# @dataclass
# class OrcaConfig:
#     coords: Coords
#     kwlines: List[KWLine] = None
#     orca_geom: Optional[OrcaGeom] = None
