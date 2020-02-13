"""basic tests"""
import dclab
import numpy as np
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox

from dckit.main import DCKit


from helper_methods import retrieve_data, cleanup


def test_simple(qtbot):
    """Open the main window and close it again"""
    main_window = DCKit(check_update=False)
    main_window.close()


def test_list_entries(qtbot):
    mw = DCKit(check_update=False)
    qtbot.addWidget(mw)
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    mw.append_paths([path])
    meta = mw.get_metadata(0)
    assert meta["experiment"]["sample"] == "calibration_beads"


def test_task_compress(qtbot, monkeypatch):
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    path_out = path.with_name("compressed")
    path_out.mkdir()
    # Monkeypatch
    monkeypatch.setattr(QDialog, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                        lambda *args: str(path_out))

    mw = DCKit(check_update=False)
    qtbot.addWidget(mw)
    mw.append_paths([path])
    pouts, invalid = mw.on_task_compress()
    assert len(pouts) == 1
    assert len(invalid) == 0
    with dclab.new_dataset(pouts[0]) as ds, dclab.new_dataset(path) as ds0:
        assert len(ds) == len(ds0)
        for feat in dclab.dfn.scalar_feature_names:
            if feat in ds or feat in ds0:
                assert feat in ds0
                assert feat in ds
                assert np.all(ds[feat] == ds0[feat])
    cleanup()


def test_task_join(qtbot, monkeypatch):
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    path_out = path.with_name("out.rtdc")
    # Monkeypatch
    monkeypatch.setattr(QDialog, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QFileDialog, "getSaveFileName",
                        lambda *args: (str(path_out), None))

    mw = DCKit(check_update=False)
    qtbot.addWidget(mw)
    mw.append_paths([path, path])
    mw.on_task_join()
    with dclab.new_dataset(path_out) as ds, dclab.new_dataset(path) as ds0:
        assert len(ds) == 2*len(ds0)
    cleanup()


def test_task_metadata_sample(qtbot, monkeypatch):
    # Monkeypatch message box to always return OK
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    mw = DCKit(check_update=False)
    qtbot.addWidget(mw)
    path = retrieve_data("rtdc_data_hdf5_rtfdc.zip")
    mw.append_paths([path])
    mw.tableWidget.item(0, 3).setText("Peter Pan")
    mw.on_task_metadata()
    with dclab.new_dataset(path) as ds:
        assert ds.config["experiment"]["sample"] == "Peter Pan"
    cleanup()


def test_task_tdms2rtdc(qtbot, monkeypatch):
    path = retrieve_data("rtdc_data_traces_video.zip")
    path_out = path.with_name("converted")
    path_out.mkdir()
    # Monkeypatch message box to always return OK
    monkeypatch.setattr(QMessageBox, "exec_", lambda *args: QMessageBox.Ok)
    monkeypatch.setattr(QFileDialog, "getExistingDirectory",
                        lambda *args: str(path_out))
    mw = DCKit(check_update=False)
    qtbot.addWidget(mw)
    mw.append_paths([path])
    assert mw.tableWidget.rowCount() == 1
    paths_converted, invalid, errors = mw.on_task_tdms2rtdc()
    assert len(errors) == 0
    assert len(invalid) == 0
    assert len(paths_converted) == 1
    with dclab.new_dataset(paths_converted[0]) as ds:
        assert ds.config["setup"]["module composition"] == "Cell_Flow_2, Fluor"
    cleanup()
