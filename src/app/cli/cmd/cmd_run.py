import click
from loguru import logger
from app.cli.start import Environment, pass_environment


@click.command("run", short_help="Run the CLI application.")
@pass_environment
def cli(ctx: Environment):
    """Run the CLI application."""
    logger.success(f'The command "run" was executed; debug: {ctx.debug}')
