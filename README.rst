|DCKit|
=======

|PyPI Version| |Tests Status Linux macOS| |Tests Status Win| |Coverage Status|


**DCKit** is a graphical toolkit for performing several data editing
tasks that would otherwise be only available via the
`dclab command-line interface <https://dclab.readthedocs.io/en/stable/sec_cli.html>`__
or (for the .rtdc file format) via external tools such as
`HDFView <https://www.hdfgroup.org/downloads/hdfview/>`__.


Installation
------------
A Windows installer is available from the
`release page <https://github.com/ZELLMECHANIK-DRESDEN/DCKit/releases>`__.
If you have Python 3 installed, you may also use pip to install DCKit:
::

    # install dckit
    pip install dckit
    # run dckit
    dckit


Usage
-----
The interface is mostly self-explanatory. Add measurements via the options
in the ``File`` menu or by drag-and-dropping files into DCKit. You may edit
entries in the ``Sample`` column and apply the changes via the
``Update sample names`` button on the right.


Testing
-------

::

    pip install -e .
    python setup.py test
    

.. |DCKit| image:: https://raw.github.com/ZELLMECHANIK-DRESDEN/DCKit/master/docs/logo/dckit_h50.png
.. |PyPI Version| image:: https://img.shields.io/pypi/v/dckit.svg
   :target: https://pypi.python.org/pypi/dckit
.. |Tests Status Win| image:: https://img.shields.io/appveyor/ci/paulmueller/DCKit/master.svg?label=build_win
   :target: https://ci.appveyor.com/project/paulmueller/DCKit
.. |Tests Status Linux macOS| image:: https://img.shields.io/travis/ZELLMECHANIK-DRESDEN/DCKit.svg?label=tests_linux_macos
   :target: https://travis-ci.org/ZELLMECHANIK-DRESDEN/DCKit
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/ZELLMECHANIK-DRESDEN/DCKit/master.svg
   :target: https://codecov.io/gh/ZELLMECHANIK-DRESDEN/DCKit
