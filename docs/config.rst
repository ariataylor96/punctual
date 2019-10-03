config.json
===========

Required data
-------------

There is nothing in the `config.json` file that is required to be there - as long as it can be parsed as JSON and exists, then you're good to go.

Currently no options conflict with any other options, so any configuration is viable. Below is a sample file that uses all available options.

Sample
------
.. code-block:: json

   {
     "links": {
        "rofi-config.txt": "~/.config/rofi/config"
     },
     "packages": [
        "themes"
     ],
     "hooks": {
        "pre_install": "echo 'Pre install'",
        "post_install": "echo 'Post install'",

        "pre_delete": "echo 'Pre delete'",
        "post_delete": "echo 'Post delete'"
     },
     "autolink": false,
     "autodiscover": true,
     "force": true
   }


Keys
----

:param links: A dict declaring which symlinks to create on the file system - package filenames are relative to the package root (`{"package-filename": "~/local/file/name"}`)
:param packages: A list of sub-packages contained in this package
:param hooks: Shell commands to execute during `pre/post` install and `pre/post` delete
:param autolink: If `true`, detects files and directories inside of the package and links them to the user's home folder.
:param autodiscover: If `true`, treats all subdirectories of the current package as a sub package. Useful for having a root package automatically detect all other packages without manual declaration.
:param force: Whether existing files should be removed during installation. This takes precedence over the CLI flag.
