Getting Started
===============

After installing `punctual` from pip, you'll have access to the `pcl` command line tool. Using this, you can `install`, `delete`, or `list` your dotfile packages. We'll go over what packages look like and how to create packages in the next later section.

.. _Env_Var:

Setting your Package Root
-------------------------
You must manually set the environment variable `$PUNCTUAL_PACKAGE_DIR` to the location of your dotfile packages. If not set, this defaults to `~/dotfiles`.

Programmatic Usage
------------------
`punctual` exposes all of its internal functionality in pure Python and can be imported without side effects. Please see :doc:`modules/punctual` for details.
