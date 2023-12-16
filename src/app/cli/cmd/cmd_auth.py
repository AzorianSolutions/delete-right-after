import click
from app.cli.start import Environment, pass_environment


@click.command("auth", short_help="Run the account authorization process.")
@pass_environment
def cli(ctx: Environment):
    """Run the account authorization process."""
    from app.lib.azure.managers import AzureManager
    from . import setup_logging
    setup_logging(ctx.settings)
    manager: AzureManager = AzureManager(ctx.settings)
    manager.auth()
