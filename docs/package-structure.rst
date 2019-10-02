Package Structure
=================

What is a package?
------------------
A package is any directory that contains a `config.json` file.

`punctual` requires that your packages share a single root directory (see :ref:`Env_Var`), which does not necessarily have to be a package as well.


Notes
-----
For the `list` command to work properly, your root directory will need to be a package that at minimum declares its own subpackages.

There are other associated benefits to having your package root be a package itself - by running `pcl install .` or `pcl delete .` you can immediately install or delete all of your dotfile packages with a single command.

You can also declare global hooks in this root package.
