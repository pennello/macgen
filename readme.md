Description
-----------
`macgen` generates a random and correctly-formatted MAC address. The
last three octets are always random.  You may choose whether or not you
want to use an organizationally unique identifier (OUI); by default, one
is used..  If not using an OUI, you may choose whether or not your MAC
address has its locally administered bit set, by default, it won't.
Default output is a sequence of two-digit hex values for each octet,
separated by `:` characters.  You may choose to omit the `:` characters,
or, if you like, output the MAC address as raw bytes.  Finally, there is
an option to output verbose debug information to standard error.

In order to choose real OUIs, `macgen` will fetch an official listing
from the IEEE.  The listing will be cached locally (see the Files
section), and if it becomes too old, it will be re-fetched.

Build & Installation
--------------------
Simply run `make && sudo make install`.  The `Makefile` takes advantage
of GNU extensions; therefore, you will want to use `gmake` on FreeBSD.
The `Makefile` supports `DESTDIR`.

`make test` will run tests in the `test` directory, finding any unit
tests there whose names match `test*.py` (the default for `unittest
discover`) and running them.  `src` is automatically added to the import
path for any tests.  Note that test code is _not_ incorporated into
`macgen`.

`make uninstall` will uninstall.  Note that the local OUI cache file
(see the Files section) will not be uninstalled automatically for you.

Documentation
-------------
`macgen` has a healthy amount of command-line help.  Run `macgen -h` to
get started.

In addition, most of the classes and methods have Pydoc documentation.

Files
-----
 - `/usr/local/bin/macgen` (via `make install`)
 - `$HOME/var/cache/macgen/oui` (created at runtime)

The OUI cache will be stored in the XDG cache home if available.
