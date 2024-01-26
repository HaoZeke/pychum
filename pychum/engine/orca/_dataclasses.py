from dataclasses import dataclass, field
from typing import List, Optional, Dict
from pathlib import Path
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
class FreeEndSettings:
    use: bool = False
    opt_type: str = "PERP"
    ec: float = 0.0
    ec_end: float = 0.0
    kappa: float = 1.0

    def __post_init__(self):
        valid_opt_types = {"PERP", "CONTOUR", "FULL"}
        if self.opt_type.upper() not in valid_opt_types:
            raise ValueError(
                f"opt_type must be one of {valid_opt_types}, got '{self.opt_type}'"
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
class SpringSettings:
    spring_kind: str = "image"
    const1: float = 0.01
    const2: float = 0.1
    energy_weighted: bool = True
    perpspring: str = "no"
    llt_cos: bool = True

    def __post_init__(self):
        valid_springkinds = {"image", "dof", "ideal"}
        valid_perpsprings = {"no", "cos", "tan", "cosTan", "DNEB"}
        if self.spring_kind.lower() not in valid_springkinds:
            raise ValueError(
                f"spring_kind must be one of {valid_springkinds}, got '{self.spring_kind}'"
            )
        if self.perpspring.lower() not in valid_perpsprings:
            raise ValueError(
                f"perpstring must be one of {valid_perpsprings}, got '{self.perpspring}'"
            )


@dataclass
class RestartSettings:
    gbw_basename: str = None
    allxyz: str = None

    def __post_init__(self):
        if self.gbw_basename and self.allxyz:
            raise ValueError("Only one of gbw_basename or allxyz should be provided.")


@dataclass
class TSGuessSettings:
    xyz_struct: str = None
    pdb_struct: str = None
    ts_img: int = -1

    def __post_init__(self):
        if self.xyz_struct and self.pdb_struct:
            raise ValueError("Only one of xyz_struct or pdb_struct should be provided.")


@dataclass
class FixCenterSettings:
    active: bool = True
    remove_extern_force: bool = True


@dataclass
class NebBlock(OrcaBlock):
    end_xyz: str
    nimgs: int
    convtype: str = "CIONLY"
    printlevel: int = 4
    neb_ts: bool = False
    neb_ci: bool = False
    quatern: str = "ALWAYS"
    climbingimage: bool = True
    check_scf_conv: bool = True
    preopt: bool = False
    nsteps_foundintermediate: int = 30
    abortif_foundintermediate: bool = False
    npts_interpol: int = 10
    interpolation: str = "IDPP"
    tangent: str = "IMPROVED"

    lbfgs_settings: LBFGSSettings = field(default_factory=LBFGSSettings)
    fire_settings: FIRESettings = field(default_factory=FIRESettings)
    reparam_settings: ReparamSettings = field(default_factory=ReparamSettings)
    idpp_settings: IDPPSettings = field(default_factory=IDPPSettings)
    zoom_settings: ZoomSettings = field(default_factory=ZoomSettings)
    optim_settings: OptimSettings = field(default_factory=OptimSettings)
    convtol_settings: ConvTolSettings = field(default_factory=ConvTolSettings)
    free_end_settings: FreeEndSettings = field(default_factory=FreeEndSettings)
    spring_settings: SpringSettings = field(default_factory=SpringSettings)
    restart_settings: RestartSettings = field(default_factory=RestartSettings)
    tsguess_settings: TSGuessSettings = field(default_factory=TSGuessSettings)
    fix_center_settings: FixCenterSettings = field(default_factory=FixCenterSettings)

    def __post_init__(self):
        valid_convtypes = {"all", "cionly"}
        valid_quaterns = {"no", "startonly", "always"}
        valid_tangents = {"improved", "original"}
        valid_interpolations = {"IDPP", "LINEAR", "XTB1TS", "XTB1", "XTB2TS", "XTB2"}
        if self.convtype.lower() not in valid_convtypes:
            raise ValueError(
                f"Convergence type must be one of {valid_convtypes}, got '{self.convtype}'"
            )
        if self.quatern.lower() not in valid_quaterns:
            raise ValueError(
                f"quatern must be one of {valid_quaterns}, got '{self.quatern}'"
            )
        if self.tangent.lower() not in valid_tangents:
            raise ValueError(
                f"tangent must be one of {valid_tangents}, got '{self.tangent}'"
            )
        if self.interpolation.upper() not in valid_interpolations:
            raise ValueError(
                f"interpolation must be one of {valid_interpolations}, got '{self.interpolation}'"
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
