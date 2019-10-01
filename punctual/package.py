import json
from subprocess import run

from .utils import use_dir, root_package_dir, join
from .link import Link


class Package:
    """
    An object representing a dotfile package.

    :param package_name: The directory name of the package to load
    :param force: Whether or not to force installation
    """

    def __init__(self, package_name, force=False):
        self.package_dir = join(root_package_dir, package_name)
        package_config = {}

        with use_dir(self.package_dir):
            with open('config.json', 'r') as f:
                package_config = json.load(f)

            self.links = [
                Link(src, dest)
                for src, dest in package_config.get('links', {}).items()
            ]

            self.sub_packages = [
                Package(join(package_name, sub_package_name), force=force)
                for sub_package_name in package_config.get('packages', [])
            ]

            self.hooks = {
                'pre_install': None,
                'post_install': None,

                'pre_delete': None,
                'post_delete': None,
            }

            self.hooks.update(package_config.get('hooks', {}))

            self.force = package_config.get('force', force)

    def _call_hook(self, name):
        hook = self.hooks[name]

        if hook:
            run(hook, shell=True)

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
