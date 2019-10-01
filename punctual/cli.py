import click

from .utils import check_directory
from .package import Package


@click.group()
def cli():
    pass


@cli.command()
@click.argument('package_name')
@click.option('--force', default=False, is_flag=True)
def install(package_name, force):
    check_directory()
    Package(package_name, force=force).install()


@cli.command()
@click.argument('package_name')
def delete(package_name):
    check_directory()
    Package(package_name).delete()
