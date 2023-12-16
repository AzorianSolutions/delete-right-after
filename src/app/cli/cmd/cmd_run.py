import click
from app.cli.start import Environment, pass_environment
from app.config import settings


@click.command('run', short_help='Run the mail scrubbing process.')
@click.option('--debug', '-d', is_flag=True, default=settings.debug,
              help='Defines whether this should be ran in debug mode.')
@click.option('--delete', '-del', is_flag=True, default=False,
              help='Delete emails instead of just marking them as read.')
@click.option('--dry-run', '-dr', is_flag=True, default=settings.dry_run,
              help='Defines whether this should be ran in dry run mode.')
@pass_environment
def cli(ctx: Environment, debug: bool = False, delete: bool = False, dry_run: bool = False):
    """Run the mail scrubbing process."""
    from app.lib.azure.managers import AzureManager
    from . import setup_logging

    ctx.settings.debug = debug
    ctx.settings.dry_run = dry_run

    setup_logging(ctx.settings)

    manager: AzureManager = AzureManager(ctx.settings)
    manager.scrub_mail(delete=delete)
