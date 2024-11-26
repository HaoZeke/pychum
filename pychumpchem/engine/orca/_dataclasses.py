from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class BlockType(Enum):
    NEB = "neb"
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
    isotope: float | None = None
    nuclear_charge: float | None = None
    fragment_number: int | None = None
    is_dummy: bool = False
    point_charge: float | None = None
    bond_atom: int | None = None  # Index of bonded atom (for internal coordinates)
    bond_length: float | None = None  # Bond length (for internal coordinates)
    angle_atom: int | None = None  # Index of angle atom (for internal coordinates)
    angle: float | None = None  # Bond angle (for internal coordinates)
    dihedral_atom: int | None = None  # Index of dihedral atom (for internal coordinates)
    dihedral: float | None = None  # Dihedral angle (for internal coordinates)
    is_frozen_x: bool = False  # Cartesian only
    is_frozen_y: bool = False  # Cartesian only
    is_frozen_z: bool = False  # Cartesian only

    def __post_init__(self):
        if self.point_charge is not None:
            self.symbol = "Q"
        elif self.symbol is None:
            msg = "Atom symbol is required unless it's a point charge."
            raise ValueError(msg)


@dataclass
class Coords:
    charge: int
    multiplicity: int
    fmt: str
    filedat: str = ""
    atoms: list[Atom] = field(default_factory=list)


@dataclass
class GeomScan:
    atoms: list[int]
    range: list[float]
    points: int


@dataclass
class GeomBlock(OrcaBlock):
    bonds: list[GeomScan] = field(default_factory=list)
    dihedrals: list[GeomScan] = field(default_factory=list)
    angles: list[GeomScan] = field(default_factory=list)

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
            msg = f"Interp must be one of {valid_interps}, got '{self.interp}'"
            raise ValueError(msg)


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
            msg = f"Method must be one of {valid_methods}, got '{self.method}'"
            raise ValueError(msg)


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
            msg = f"opt_type must be one of {valid_opt_types}, got '{self.opt_type}'"
            raise ValueError(msg)


@dataclass
class ZoomSettings:
    tol_turn_on: float = 0.0
    offset: int = 2
    auto: bool = True
    tol_scale: int = 10
    alpha: float = 0.5
    interpolation: str = "linear"
    printfulltrj: bool = True

    def __post_init__(self):
        valid_interpolations = {"linear", "cubic"}
        if self.interpolation.lower() not in valid_interpolations:
            msg = (
                f"interpolation must be one of {valid_interpolations},"
                " got '{self.interpolation}'"
            )
            raise ValueError(msg)


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
            msg = (
                f"spring_kind must be one of {valid_springkinds},"
                " got '{self.spring_kind}'"
            )
            raise ValueError(msg)
        if self.perpspring.lower() not in valid_perpsprings:
            msg = (
                f"perpstring must be one of {valid_perpsprings},"
                " got '{self.perpspring}'"
            )
            raise ValueError(msg)


@dataclass
class RestartSettings:
    gbw_basename: str = None
    allxyz: str = None

    def __post_init__(self):
        if self.gbw_basename and self.allxyz:
            msg = "Only one of gbw_basename or allxyz should be provided."
            raise ValueError(msg)


@dataclass
class TSGuessSettings:
    xyz_struct: str = None
    pdb_struct: str = None
    ts_img: int = -1

    def __post_init__(self):
        if self.xyz_struct and self.pdb_struct:
            msg = "Only one of xyz_struct or pdb_struct should be provided."
            raise ValueError(msg)


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
            msg = (
                f"Convergence type must be one of {valid_convtypes},"
                " got '{self.convtype}'"
            )
            raise ValueError(msg)
        if self.quatern.lower() not in valid_quaterns:
            msg = f"quatern must be one of {valid_quaterns}," " got '{self.quatern}'"
            raise ValueError(msg)
        if self.tangent.lower() not in valid_tangents:
            msg = f"tangent must be one of {valid_tangents}," " got '{self.tangent}'"
            raise ValueError(msg)
        if self.interpolation.upper() not in valid_interpolations:
            msg = (
                f"interpolation must be one of {valid_interpolations},"
                " got '{self.interpolation}'"
            )
            raise ValueError(msg)

    def block_type(self) -> BlockType:
        return BlockType.NEB


@dataclass
class OrcaConfig:
    kwlines: str
    coords: Coords
    blocks: dict[BlockType, OrcaBlock] = field(default_factory=dict)
    extra_blocks: dict[str, str] = field(default_factory=dict)

    def add_block(self, block: OrcaBlock):
        self.blocks[block.block_type()] = block


# @dataclass
# class OrcaConfig:
#     coords: Coords
#     kwlines: List[KWLine] = None
#     orca_geom: Optional[OrcaGeom] = None
