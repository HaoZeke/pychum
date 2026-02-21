import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

from pychum.engine.orca._dataclasses import OrcaConfig


class OrcaInputRenderer:
    def __init__(self, config: OrcaConfig):
        self.config = config
        # Determine the package path to access the templates
        package_path = os.path.dirname(os.path.abspath(__file__))
        template_dir = os.path.join(package_path, "_blocks")
        self.env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(enabled_extensions=("toml")),
        )
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.rstrip_blocks = True

    def render(self, template_name: str):
        template = self.env.get_template(template_name)
        context = {
            "config": self.config,
        }
        return template.render(context).replace("\n\n", "\n")
