import shutil
import tempfile
import time

from PyQt5 import QtCore


TMPDIR = tempfile.mkdtemp(prefix=time.strftime(
    "dckit_test_%H.%M_"))

pytest_plugins = ["pytest-qt"]


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    tempfile.tempdir = TMPDIR
    QtCore.QCoreApplication.setOrganizationName("DC-Analysis")
    QtCore.QCoreApplication.setOrganizationDomain("dc.readthedocs.io")
    QtCore.QCoreApplication.setApplicationName("DCKit")
    QtCore.QSettings.setDefaultFormat(QtCore.QSettings.IniFormat)
    settings = QtCore.QSettings()
    settings.setIniCodec("utf-8")
    settings.setValue("check for updates", 0)
    settings.sync()


def pytest_unconfigure(config):
    """
    called before test process is exited.
    """
    shutil.rmtree(TMPDIR, ignore_errors=True)
