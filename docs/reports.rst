.. Copyright (c) 2015 Pietro Albini <pietro@pietroalbini.io>
   Released under the MIT license

.. _reports:

~~~~~~~~~~~~~~~~~~
Generating reports
~~~~~~~~~~~~~~~~~~

The main purpose of trackdeps is to generate reports about pinned dependencies
in your projects. Reports are statically builded by the ``trackdeps-report``
command-line utility from a configuration file, and they're contained in a
single minified HTML file. This means you can publish it by simply copying the
file to your webserver's document root.

.. _reports-config:

The configuration file
======================

Reports are generated using a YAML configuration file, which defines where to
look for pinned dependencies.

Let's say we have two git repositories (``repo1`` for *project1* and ``repo2``
for *project2* hosted on ``git.example.com``), and each of them has pinned
dependencies on ``setup.py`` and ``requirements.txt``. Also, *project2* has
multiple requirements files matching the glob expression
``requirements-*.txt``. A configuration file in this case looks like this:

.. code-block:: yaml

   project1:
     git-url: git@git.example.com:repo1.git
     setup: setup.py
     requirements:
     - requirements.txt

   project2:
     git-url: git@git.example.com:repo2.git
     setup: setup.py
     requirements:
     - requirements.txt
     - requirements-*.txt

Now let's break down that configuration:

* Each project has its own top-level section, named as the project. The project
  name you provide will be used in the generated report in order to tell you
  where you should update a package.
* You must provide a valid git URL, from which dependencies will be fetched.
  You can use any URL git's ``clone`` command support.
* You can define a single ``setup.py`` per project, and multiple
  ``requirements.txt``-style files in a single project. All this fields
  supports glob expressions.

.. _reports-generate:

Generation of the report
========================

Now that you have your configuration file, you can generate the report (make
sure trackdeps is :ref:`installed correctly <install>`)::

   $ trackdeps-report path/to/config.yml

The report will dumped to the standard output. If you want to save it in a
custom location you can use the ``-o`` flag. The command also refuses to
overwrite an existing file, but you can disable this behavior with the ``-f``
flag::

   $ trackdeps-report path/to/config.yml -o custom/output.html -f
