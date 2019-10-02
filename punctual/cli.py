from colorama import Fore, Style
import click

from .utils import check_directory
from .package import Package


@click.group()
def cli():
    pass


@cli.command()
@click.argument('package_name')
@click.option(
    '--force',
    default=False,
    is_flag=True,
    help='Remove any existing files',
)
def install(package_name, force):
    check_directory()
    Package(package_name, force=force).install()


@cli.command()
@click.argument('package_name')
def delete(package_name):
    check_directory()
    Package(package_name).delete()


@cli.command()
def list():
    names = []
    statuses = []

    longest_name = 0
    for package in Package('.').sub_packages:
        if len(package.name) > longest_name:
            longest_name = len(package.name)

        names.append(
            f'{Fore.BLUE}{Style.BRIGHT}{package.name}{Style.RESET_ALL}',
        )
        statuses.append(package.status_text)

    for name, status in zip(names, statuses):
        click.echo(f'{name.ljust(longest_name)} -> {status}')
