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
            optim_settings = None
            if "optim" in neb_data:
                optim_settings = OptimSettings(**neb_data.pop("optim"))
            lbfgs_settings = None
            if "lbfgs" in neb_data:
                lbfgs_settings = LBFGSSettings(**neb_data.pop("lbfgs"))
            fire_settings = None
            if "fire" in neb_data:
                fire_settings = FIRESettings(**neb_data.pop("fire"))
            idpp_settings = None
            if "idpp" in neb_data:
                idpp_settings = IDPPSettings(**neb_data.pop("idpp"))
            zoom_settings = None
            if "zoom" in neb_data:
                zoom_settings = ZoomSettings(**neb_data.pop("zoom"))
            reparam_settings = None
            if "reparam" in neb_data:
                reparam_settings = ReparamSettings(**neb_data.pop("reparam"))
            convtol_settings = None
            if "convtol" in neb_data:
                convtol_settings = ConvTolSettings(**neb_data.pop("convtol"))

            blocks["neb"] = NebBlock(
                fire_settings=fire_settings,
                lbfgs_settings=lbfgs_settings,
                idpp_settings=idpp_settings,
                zoom_settings=zoom_settings,
                reparam_settings=reparam_settings,
                optim_settings=optim_settings,
                convtol_settings=convtol_settings,
                **neb_data,
            )

        return OrcaConfig(coords=coords, blocks=blocks)

        # # Create the final OrcaConfig instance
        # if engine == 'orca':
        #     return OrcaConfig(coords=coords,
        #                       orca_geom=orca_geom)
        # else:
        #     raise(ValueError("Only Orca is supported for now"))
