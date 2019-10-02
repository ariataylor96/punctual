config.json
===========

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
     "force": true
   }


Keys
----

:param links: A dict declaring which symlinks to create on the file system - package filenames are relative to the package root (`{"package-filename": "~/local/file/name"}`)
:param packages: A list of sub-packages contained in this package
:param hooks: Shell commands to execute during `pre/post` install and `pre/post` delete
:param force: Whether existing files should be removed during installation. This takes precedence over the CLI flag.
