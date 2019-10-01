from colorama import Fore, Style
from contextlib import contextmanager
import click
import os
import sys

root_package_dir = os.path.expanduser(
    os.getenv('PUNCTUAL_PACKAGE_DIR', '~/dotfiles'),
)

# Just an alias to save me from typing the full path every time
join = os.path.join


@contextmanager
def use_dir(new_dir):
    """
    Goes into the new directory, yields, and changes back when done

    :param new_dir: The directory to change to
    """
    owd = os.getcwd()
    os.chdir(new_dir)

    try:
        yield
    finally:
        os.chdir(owd)


def check_directory():
    if os.getenv('PUNCTUAL_PACKAGE_DIR', None) is None:
        click.echo(f'$PUNCTUAL_PACKAGE_DIR is unset, using {root_package_dir}')

    if not os.path.lexists(root_package_dir):
        click.echo(f'{root_package_dir} does not exist. Exiting with error.')
        sys.exit(1)


def print_status_output(text, color=''):
    def inner():
        click.echo(f'{color}{Style.BRIGHT}{text}{Style.RESET_ALL}')

    return inner


def logs(text):
    return print_status_output(text, color=Fore.GREEN)


def loge(text):
    return print_status_output(text, color=Fore.RED)


def log(text):
    return print_status_output(text)
