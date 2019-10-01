import os


class Link:
    """
    An object representing a link from a package.

    :param src: Name of the source file, relative to the package root
    :param dest: Path to the destination file
    """

    def __init__(self, src, dest):
        self.src = os.path.realpath(src)
        self.dest = os.path.abspath(os.path.expanduser(dest))

    @property
    def exists(self):
        """
        Whether or not the file currently exists.
        """
        return os.path.lexists(self.dest)

    def delete(self):
        """
        Remove the specified link.
        """

        os.remove(self.dest)

    def install(self, force=False):
        """
        Create the specified link

        :param force: Do not error out if the file exists
        :raises FileExistsError: if the link already exists
        """
        if self.exists:
            if not force:
                raise FileExistsError(
                    f'{self.dest} exists, and force is not specified',
                )

            self.delete()

        os.makedirs(os.path.dirname(self.dest), exist_ok=True)
        os.symlink(self.src, self.dest)
