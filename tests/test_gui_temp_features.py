from dclab.rtdc_dataset.feat_temp import deregister_all
import h5py
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
import pytest

from dckit.main import DCKit
from dckit.preferences import register_temporary_features

from helper_methods import retrieve_data


@pytest.fixture(autouse=True)
def run_around_tests():
    # Code that will run before your test, for example:
    pass
    # A test function will be run at this point
    yield
    # Code that will run after your test, for example:
    # Remove all temporary features
    deregister_all()
    settings = QtCore.QSettings()
    settings.remove("included features")


def test_task_compress_with_scalar_feature(qtbot, monkeypatch):
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    path_out = path.with_name("compressed")
    path_out.mkdir()
    # Monkeypatch
    monkeypatch.setattr(QDialog, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                        lambda *args: str(path_out))

    # add a temporary feature to the dataset
    with h5py.File(path, "a") as h5:
        data = np.linspace(2, 3, len(h5["events/deform"]))
        h5["events/peter"] = data

    mw = DCKit()
    qtbot.addWidget(mw)
    mw.append_paths([path])

    # Without any registered temporary features, the "peter" feature
    # will not be available.
    paths_cmp, _ = mw.on_task_compress()

    with h5py.File(paths_cmp[0], "r") as h5:
        assert "peter" not in h5["events"]

    # If we register the "peter" feature, then it should also be exported.
    settings = QtCore.QSettings()
    settings.setValue("included features", "peter")
    settings.setValue("feature scalar peter", "1")
    paths_cmp[0].unlink()
    register_temporary_features()
    mw.on_task_compress()

    with h5py.File(paths_cmp[0], "r") as h5:
        assert "peter" in h5["events"]
        assert np.all(data == h5["events/peter"])


def test_task_compress_with_non_scalar_feature(qtbot, monkeypatch):
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    path_out = path.with_name("compressed")
    path_out.mkdir()
    # Monkeypatch
    monkeypatch.setattr(QDialog, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                        lambda *args: str(path_out))

    # add a temporary feature to the dataset
    with h5py.File(path, "a") as h5:
        data = np.zeros((len(h5["events/deform"]), 2, 5, 3))
        data[1, 0, 3, 1] = 10
        h5["events/hans"] = data

    mw = DCKit()
    qtbot.addWidget(mw)
    mw.append_paths([path])

    # Without any registered temporary features, the "hans" feature
    # will not be available.
    paths_cmp, _ = mw.on_task_compress()

    with h5py.File(paths_cmp[0], "r") as h5:
        assert "hans" not in h5["events"]

    # If we register the "hans" feature, then it should also be exported.
    settings = QtCore.QSettings()
    settings.setValue("included features", "hans")
    settings.setValue("feature scalar hans", "0")
    paths_cmp[0].unlink()
    register_temporary_features()
    mw.on_task_compress()

    with h5py.File(paths_cmp[0], "r") as h5:
        assert "hans" in h5["events"]
        assert np.all(data == h5["events/hans"])
