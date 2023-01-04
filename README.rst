|DCKit|
=======

|PyPI Version| |Build Status Unix| |Build Status Win| |Coverage Status|


**DCKit** is a graphical toolkit for performing several data editing
tasks that would otherwise be only available via the
`dclab command-line interface <https://dclab.readthedocs.io/en/stable/sec_cli.html>`__
or (for the .rtdc file format) via external tools such as
`HDFView <https://www.hdfgroup.org/downloads/hdfview/>`__.


Installation
------------
A Windows installer and macOS packages are available from the
`release page <https://github.com/DC-analysis/DCKit/releases>`__.
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
    python -m pytest tests


.. |DCKit| image:: https://raw.github.com/DC-analysis/DCKit/master/docs/logo/dckit_h50.png
.. |PyPI Version| image:: https://img.shields.io/pypi/v/dckit.svg
   :target: https://pypi.python.org/pypi/dckit
.. |Build Status Unix| image:: https://img.shields.io/github/actions/workflow/status/DC-analysis/DCKit/check.yml
   :target: https://github.com/DC-analysis/DCKit/actions?query=workflow%3AChecks
.. |Build Status Win| image:: https://img.shields.io/appveyor/build/paulmueller/dckit
   :target: https://ci.appveyor.com/project/paulmueller/DCKit
.. |Coverage Status| image:: https://img.shields.io/codecov/c/github/DC-analysis/DCKit/master.svg
   :target: https://codecov.io/gh/DC-analysis/DCKit
