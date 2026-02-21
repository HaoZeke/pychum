import os
from jinja2 import Environment, FileSystemLoader

from pychum.engine.eon._dataclasses import NWChemSocketConfig

class NWChemRenderer:
    def __init__(self, config: NWChemSocketConfig):
        self.config = config
        package_path = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(package_path, "_blocks")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
        )
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True

    def render(self, template_name: str):
        template = self.env.get_template(template_name)
        context = {
            "config": self.config,
        }
        return template.render(context)
