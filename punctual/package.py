from colorama import Fore, Style
import json
import os
from subprocess import run

from .utils import use_dir, root_package_dir, join, logs, log
from .link import Link


class Package:
    """
    An object representing a dotfile package.

    :param package_name: The directory name of the package to load
    :param force: Whether or not to force installation
    """

    def __init__(self, package_name, force=False):
        self.package_dir = join(root_package_dir, package_name)
        self.package_name = package_name
        self.name = os.path.basename(package_name)
        self.force = force
        package_config = {}

        with use_dir(self.package_dir):
            with open('config.json', 'r') as f:
                package_config = json.load(f)

            self.include_hidden = package_config.get('includeHidden', False)

            self.links = [
                Link(src, dest)
                for src, dest in package_config.get('links', {}).items()
            ]
            self._autolink(package_config)

            self.sub_packages = [
                Package(join(package_name, sub_package_name), force=force)
                for sub_package_name in package_config.get('packages', [])
            ]
            self._autodiscover_packages(package_config)

            self.hooks = {
                'pre_install': log(f'Initiating install of {self.name}'),
                'post_install': logs(f'Installed {self.name}'),

                'pre_delete': log(f'Initiating deletion of {self.name}'),
                'post_delete': logs(f'Deleted {self.name}'),
            }

            self.hooks.update(package_config.get('hooks', {}))

            self.force = package_config.get('force', force)

    def _call_hook(self, name):
        hook = self.hooks[name]

        if callable(hook):
            hook()
        elif isinstance(hook, str):
            run(hook, shell=True)

    def _in_existing_links(self, name):
        existing_links = set([l.src for l in self.links])

        return name in existing_links

    def _autodiscover_packages(self, package_config):
        if not package_config.get('autodiscover', False):
            return

        def _is_sub_package(f):
            if not f.is_dir():
                return False

            if f.name.startswith('.') and not self.include_hidden:
                return False

            if self._in_existing_links(f.name):
                return False

            with use_dir(f.name):
                return 'config.json' in [g.name for g in os.scandir()]

        sub_packages = [
            Package(join(self.package_name, f.name), force=self.force)
            for f in os.scandir()
            if _is_sub_package(f)
        ]

        self.sub_packages += sub_packages

    def _autolink(self, package_config):
        if not package_config.get('autolink', False):
            return

        links = [
            Link(f.name, join(os.path.expanduser('~/'), f.name))
            for f in os.scandir()
            if f.name != 'config.json' and not self._in_existing_links(f.name)
        ]

        self.links += links

    @property
    def installed(self):
        return all([link.exists for link in self.links])

    @property
    def status_text(self):
        if self.installed:
            return f'{Fore.GREEN}{Style.BRIGHT}installed{Style.RESET_ALL}'

        return f'{Fore.RED}{Style.BRIGHT}not installed{Style.RESET_ALL}'

    def install(self):
        """
        Installs the package, top level links, and sub packages.
        """
        with use_dir(self.package_dir):
            self._call_hook('pre_install')

            for link in self.links:
                link.install(force=self.force)

            for sub_package in self.sub_packages:
                sub_package.install()

            self._call_hook('post_install')

    def delete(self):
        """
        Deletes the package, top level links, and sub packages.
        """
        with use_dir(self.package_dir):
            self._call_hook('pre_delete')

            for link in self.links:
                link.delete()

            for sub_package in self.sub_packages:
                sub_package.delete()

            self._call_hook('post_delete')
