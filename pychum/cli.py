from pathlib import Path

import click

from pychum.engine.orca._renderer import OrcaInputRenderer
from pychum.engine.orca.config_loader import ConfigLoader


@click.command()
@click.argument("toml_path", type=click.Path(exists=True))
@click.option(
    "--output",
    "-o",
    default=None,
    type=click.Path(),
    is_flag=False,
    flag_value="orca.inp",
    help='Output file name (default is "orca.inp").',
)
def render_orca_input(toml_path, output):
    """
    Render an Orca input file from a TOML configuration.

    TOML_PATH is the path to the TOML configuration file.
    """
    config_loader = ConfigLoader(Path(toml_path))
    config = config_loader.load_config()
    renderer = OrcaInputRenderer(config)
    rendered_output = renderer.render("base.jinja")

    if output is not None:
        with open(output, "w") as file:
            file.write(rendered_output)
        click.echo(f"Rendered ORCA input file written to '{output}'")
    else:
        click.echo(rendered_output)


if __name__ == "__main__":
    render_orca_input()
