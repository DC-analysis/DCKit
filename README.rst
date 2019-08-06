|DCKit|
=======

|PyPI Version| |Status Win|


**DCKit** is a graphical toolkit for performing several tasks that
would otherwise be only available via the
dclab command line interface or via external tools such as HDFView.


Installation
------------
A Windows installer is available from the release page.
If you have Python 3 installed, you may also use pip to install DCKit:
::

    # install dckit
    pip install dckit
    # run dckit
    dckit


Usage
-----
The interface is mostly self-explanatory. Add measurements via the options
in the ``File`` menu or by drag-and-droping files into DCKit. You may edit
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
.. |Status Win| image:: https://img.shields.io/appveyor/ci/paulmueller/DCKIT/master.svg
   :target: https://ci.appveyor.com/project/paulmueller/DCKit

