import pytest
from pychum.engine.orca._dataclasses import (
    NebBlock,
    IDPPSettings,
    RestartSettings,
    Coords,
    OrcaConfig,
)
from pychum.engine.orca._renderer import OrcaInputRenderer

# Helper function to render the NebBlock
default_kwline = "!NEB-CI\n!ENGRAD UHF NOSOSCF def2-SVP"


def render_neb_block(neb_block):
    coords = Coords(charge=0, multiplicity=1, fmt="xyz")
    blocks = dict()
    blocks["neb"] = neb_block
    config = OrcaConfig(kwlines=default_kwline, coords=coords, blocks=blocks)
    renderer = OrcaInputRenderer(config)
    return str(renderer.render("base.jinja")).strip()


default_expectation = """!NEB-CI
!ENGRAD UHF NOSOSCF def2-SVP
%neb
    neb_end_xyzfile  "prod.xyz"
    nimages  8
    convtype  CIONLY
    printlevel  4
    neb_ts  false
    neb_ci  false
    quatern  ALWAYS
    climbingimage  true
    CheckSCFConv True
    PreOpt False
    NSteps_FoundIntermediate 30
    AbortIf_FoundIntermediate False
    npts_interpol 10
    interpolation  IDPP
    tangent  IMPROVED

    NEB_TS_Image -1

    Fix_center  true
    Remove_extern_force  true


    springtype image
    springconst  0.01
    springconst2  0.1
    energy_weighted True
    perpspring no
    llt_cos True

    free_end False
    free_end_type  PERP
    free_end_ec 0.0
    free_end_ec_end 0.0
    free_end_kappa 1.0

    tol_maxfp_i  0.005
    tol_rmsfp_i  0.003
    tol_maxf_ci  0.0005
    tol_rmsf_ci  0.0003
    tol_turn_on_ci  0.02
    tol_scale  10

    reparam_type  linear
    reparam 0
    tol_reparam 0.0

    opt_method  LBFGS
    maxmove  0.2
    stepsize  1.0
    maxiter  500
    local  false

    lbfgs_mem  20
    lbfgs_dr  0.002
    lbfgs_restart_on_maxmove  true
    lbfgs_reparam_on_restart  false
    lbfgs_precondition  true

    fire_initial_damp  0.1
    fire_damp_decr  0.99
    fire_step_incr  1.1
    fire_step_decr  0.5
    fire_max_step  5.0
    fire_retention  5

    tol_turn_on_zoom  0.0
    zoom_offset  2
    zoom_auto  true
    zoom_alpha  0.5
    zoom_interpolation  linear
    zoom_printfulltrj  true

    idpp_nmax  3000
    idpp_tol_maxf  0.01
    idpp_ksp  1.0
    idpp_alpha  0.01
    idpp_maxmove  0.05
    idpp_debug  false
    idpp_quatern  true
end

* xyz 0 1
*
""".strip()


# TODO(rg): Cuz there's some idiotic whitespace character in coord.jinja
def normalize_whitespace(string):
    return " ".join(string.split())


def test_default_idpp_settings_render():
    neb_block = NebBlock(end_xyz="prod.xyz", nimgs=8)
    result = render_neb_block(neb_block)
    assert normalize_whitespace(result) == normalize_whitespace(
        default_expectation.replace("nimages  5", "nimages  8")
    )


def test_custom_idpp_settings_render():
    custom_settings = IDPPSettings(
        nmax=4000,
        tol_maxf=0.02,
        ksp=1.5,
        alpha=0.02,
        maxmove=0.1,
        debug=True,
        quatern=False,
    )
    neb_block = NebBlock(end_xyz="prod.xyz", nimgs=8, idpp_settings=custom_settings)
    result = render_neb_block(neb_block)

    expected = (
        default_expectation.replace("idpp_nmax  3000", "idpp_nmax  4000")
        .replace("idpp_tol_maxf  0.01", "idpp_tol_maxf  0.02")
        .replace("idpp_ksp  1.0", "idpp_ksp  1.5")
        .replace("idpp_alpha  0.01", "idpp_alpha  0.02")
        .replace("idpp_maxmove  0.05", "idpp_maxmove  0.1")
        .replace("idpp_debug  false", "idpp_debug  true")
        .replace("idpp_quatern  true", "idpp_quatern  false")
    )

    assert normalize_whitespace(result) == normalize_whitespace(expected)


def test_restart_settings_render():
    # Test with gbw_basename setting
    restart_settings_gbw = RestartSettings(gbw_basename="restart_file.gbw")
    neb_block_gbw = NebBlock(
        end_xyz="prod.xyz", nimgs=8, restart_settings=restart_settings_gbw
    )
    result_gbw = render_neb_block(neb_block_gbw)
    expected_gbw = default_expectation.replace(
        "\n\n    springtype image",
        '\n    Restart_GBW_BaseName "restart_file.gbw"\n\n    springtype image',
    )
    assert normalize_whitespace(result_gbw) == normalize_whitespace(expected_gbw)

    # Test with allxyz setting
    restart_settings_xyz = RestartSettings(allxyz="restart_file.xyz")
    neb_block_xyz = NebBlock(
        end_xyz="prod.xyz", nimgs=8, restart_settings=restart_settings_xyz
    )
    result_xyz = render_neb_block(neb_block_xyz)
    expected_xyz = default_expectation.replace(
        "\n\n    springtype image",
        '\n    Restart_ALLXYZFile "restart_file.xyz"\n\n    springtype image',
    )
    assert normalize_whitespace(result_xyz) == normalize_whitespace(expected_xyz)


def test_restart_settings_both_gbw_and_allxyz():
    with pytest.raises(ValueError) as excinfo:
        RestartSettings(gbw_basename="restart_file.gbw", allxyz="restart_file.xyz")
    assert "Only one of gbw_basename or allxyz should be provided" in str(excinfo.value)


def test_restart_settings_neither_gbw_nor_allxyz():
    restart_settings = RestartSettings()
    assert restart_settings.gbw_basename is None
    assert restart_settings.allxyz is None


def test_restart_settings_only_gbw():
    restart_settings = RestartSettings(gbw_basename="restart_file.gbw")
    assert restart_settings.gbw_basename == "restart_file.gbw"
    assert restart_settings.allxyz is None


def test_restart_settings_only_allxyz():
    restart_settings = RestartSettings(allxyz="restart_file.xyz")
    assert restart_settings.allxyz == "restart_file.xyz"
    assert restart_settings.gbw_basename is None
