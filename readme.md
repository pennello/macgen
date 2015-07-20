TODO
----
 - Extensive Pydoc documentation.
 - Clean up readme.
 - Remove old code.

This project provides a skeleton for a pure Python project to be
distributed as a single, self-contained executable on Unix-like systems.

Usage
-----
1. Include the contents of this project into your new workspace.
2. Set the value of the `name` variable in the `Makefile`, as well as
   the contents of `.gitignore`, if applicable, to the desired name of
   your project or executable.  The default is `helloworld`.
3. Run `make`.  You will now have an executable of that name (as well as
   a ZIP; see the Details section) in your working directory.  Running
   it will give you a "Hello, world." message.  The entry point is
   `src/__main__.py`.

`make test` will run [`unittest discover`][1] on the `test` directory,
finding any unit tests there whose names match `test*.py` (the default
for `unittest discover`) and running them.  `src` is automatically added
to the import path for any tests.  Note that test code is _not_
incorporated into the self-contained executable.

To install globally, run `make install` as the superuser.  The
`Makefile` supports [`DESTDIR`][2].  The default destination for your
executable is `/usr/local/bin`.

`make uninstall` will uninstall.

`make clean` will clean your working directory of the executable, the
ZIP, and any `.pyo` compiled Python files in `src`.

`src/header` is the header for the self-contained executable; it merely
specifies a shebang for the Python interpreter.

Portability
-----------
The `Makefile` takes advantage of GNU extensions; therefore, you will
want to use `gmake` on FreeBSD.

Details
-------
This approach uses the zipfile support of the [Python command-line
interpreter][3].

Quoting the [`zipimport` module documentation][4]:
> Any files may be present in the ZIP archive, but only files `.py` and
> `.py[co]` are available for import. ZIP import of dynamic modules
> (`.pyd`, `.so`) is disallowed. Note that if an archive only contains
> `.py` files, Python will not attempt to modify the archive by adding
> the corresponding `.pyc` or `.pyo` file, meaning that if a ZIP archive
> doesn't contain `.pyc` files, importing may be rather slow.

This approach compiles with `-OO` and includes only the bytecode files
in the ZIP archive.

[1]: https://docs.python.org/3/library/unittest.html#test-discovery
[2]: https://www.gnu.org/prep/standards/html_node/DESTDIR.html#DESTDIR
[3]: https://docs.python.org/3/using/cmdline.html
[4]: https://docs.python.org/3/library/zipimport.html
