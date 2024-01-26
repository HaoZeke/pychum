import tomli as toml
from pathlib import Path
from pychum.engine.orca._dataclasses import *

class ConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = toml.load(Path(file_path).open("rb"))

    def load_neb_block(self, data):
        return NebBlock(**data)

    def load_scf_block(self, data):
        return ScfBlock(**data)

    def load_config(self):
        # Create instances of data classes based on the TOML data
        engine = self.data.get("engine", {}).get("name", "")
        units = {
            "distance": UnitConversion(
                **self.data.get("units", {}).get("distance", {})
            ),
            "energy": UnitConversion(**self.data.get("units", {}).get("energy", {})),
        }
        filedat = self.data.get("coords", {}).get("filedat", None)
        atoms = [Atom(**atom) for atom in self.data.get("coords", {}).get("atoms", [])]
        coords = Coords(
            charge=self.data.get("coords", {}).get("charge", 0),
            multiplicity=self.data.get("coords", {}).get("multiplicity", 1),
            fmt=self.data.get("coords", {}).get("fmt", "xyz"),
            filedat=filedat,
            atoms=atoms,
        )

        # Dictionary to store loaded blocks
        blocks = {}

        # Iterate through the TOML data and load each block
        # for block_type, block_data in self.data.items():
        #     if block_type in BlockType.__members__:
        #         load_method = getattr(self, f"load_{block_type.lower()}_block")
        #         blocks[block_type] = load_method(block_data)
        if "orca" in self.data and "geom" in self.data["orca"]:
            geom_data = self.data["orca"]["geom"]
            bonds = [GeomScan(**bond) for bond in geom_data.get("bonds", [])]
            dihedrals = [
                GeomScan(**dihedral) for dihedral in geom_data.get("dihedrals", [])
            ]
            angles = [GeomScan(**angle) for angle in geom_data.get("angles", [])]
            blocks["geom"] = GeomBlock(bonds=bonds, dihedrals=dihedrals, angles=angles)

        if "orca" in self.data and "neb" in self.data["orca"]:
            neb_data = self.data["orca"]["neb"]
            neb_block_args = {}
            # Unconditionally added, via defaults if not in TOML
            if "optim" in neb_data:
                neb_block_args["optim_settings"] = OptimSettings(**neb_data.pop("optim"))
            if "lbfgs" in neb_data:
                neb_block_args["lbfgs_settings"] = LBFGSSettings(**neb_data.pop("lbfgs"))
            if "fire" in neb_data:
                neb_block_args["fire_settings"] = FIRESettings(**neb_data.pop("fire"))
            if "idpp" in neb_data:
                neb_block_args["idpp_settings"] = IDPPSettings(**neb_data.pop("idpp"))
            if "zoom" in neb_data:
                neb_block_args["zoom_settings"] = ZoomSettings(**neb_data.pop("zoom"))
            if "reparam" in neb_data:
                neb_block_args["reparam_settings"] = ReparamSettings(**neb_data.pop("reparam"))
            if "convtol" in neb_data:
                neb_block_args["convtol_settings"] = ConvTolSettings(**neb_data.pop("convtol"))
            if "free_end" in neb_data:
                neb_block_args["free_end_settings"] = FreeEndSettings(**neb_data.pop("free_end"))
            if "spring" in neb_data:
                neb_block_args["spring_settings"] = SpringSettings(**neb_data.pop("spring"))
            # Not added if not present in the TOML
            restart_settings = None
            if "restart" in neb_data:
                neb_block_args["restart_settings"] = RestartSettings(**neb_data.pop("restart"))
            tsguess_settings = None
            # if "tsguess" in neb_data:
            #     tsguess_settings = TSGuessSettings(**neb_data.pop("tsguess"))
            neb_block_args = {**neb_data, **neb_block_args}

            blocks["neb"] = NebBlock(**neb_block_args)

        return OrcaConfig(coords=coords, blocks=blocks)

        # # Create the final OrcaConfig instance
        # if engine == 'orca':
        #     return OrcaConfig(coords=coords,
        #                       orca_geom=orca_geom)
        # else:
        #     raise(ValueError("Only Orca is supported for now"))
