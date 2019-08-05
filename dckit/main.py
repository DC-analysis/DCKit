import pathlib
import pkg_resources
import signal
import sys
import traceback

import dclab
from dclab.cli import get_job_info
import h5py
import numpy as np
from PyQt5 import uic, QtCore, QtWidgets
from shapeout import meta_tool
from shapeout import __version__ as soversion

from . import history
from ._version import version as __version__


class DCKit(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        path_ui = pkg_resources.resource_filename("dckit", "main.ui")
        uic.loadUi(path_ui, self)
        self.setWindowTitle("DCKit {}".format(__version__))
        # Disable native menubar (e.g. on Mac)
        self.menubar.setNativeMenuBar(False)
        # signals
        self.pushButton_sample.clicked.connect(self.on_change_sample_names)
        self.pushButton_tdms2rtdc.clicked.connect(self.on_tdms2rtdc)
        self.pushButton_join.clicked.connect(self.on_join)
        self.tableWidget.itemChanged.connect(self.on_table_text_changed)
        # menu actions
        self.action_add.triggered.connect(self.on_add_measurements)
        self.action_add_folder.triggered.connect(self.on_add_folder)
        self.action_clear.triggered.connect(self.on_clear_measurements)
        #: contains all imported paths
        self.pathlist = []

    def append_paths(self, pathlist):
        """Append selected paths to table"""
        datas = []
        # get meta data for all paths
        for path in pathlist:
            info = {"DCKit-id": (0, len(self.pathlist)),
                    "path": (1, path),
                    "sample": (2, meta_tool.get_sample_name(path)),
                    "run index": (3, meta_tool.get_run_index(path)),
                    "flow rate": (5, meta_tool.get_flow_rate(path)),
                    }
            try:
                ec = meta_tool.get_event_count(path)
            except BaseException:  # meta-tool Python2/3 issue
                # get event count using dclab (slower)
                with dclab.new_dataset(path) as ds:
                    ec = ds.config["experiment"]["event count"]
            info["event count"] = (4, ec)
            self.pathlist.append(path)
            datas.append(info)
        # populate table widget
        for info in datas:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            for key in info:
                col, val = info[key]
                if isinstance(val, bytes):
                    val = val.decode("utf-8")
                item = QtWidgets.QTableWidgetItem("{}".format(val))
                if key == "sample":
                    # allow editing sample name
                    item.setFlags(QtCore.Qt.ItemIsEnabled
                                  | QtCore.Qt.ItemIsEditable)
                elif key == "path":
                    item.setText(pathlib.Path(val).name)
                    item.setToolTip(str(val))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                elif key == "flow rate":
                    item.setText("{:.5f}".format(val))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                else:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, col, item)

    def on_add_folder(self):
        """Search folder for RT-DC data and add to table"""
        # show a dialog for selecting folder
        path = QtWidgets.QFileDialog.getExistingDirectory()
        if not path:
            return
        # find RT-DC data using shapeout
        pathlist = meta_tool.find_data(path)
        if not pathlist:
            raise ValueError("No RT-DC data found in {}!".format(path))
        # add to list
        self.append_paths(pathlist)

    def on_add_measurements(self):
        """Select .tdms and .rtdc files and add to table"""
        # show a dialog for adding multiple single files (.tdms and .rtdc)
        pathlist, _ = QtWidgets.QFileDialog.getOpenFileNames(
            None,
            'Select RT-DC data',
            '',
            'RT-DC data (*.tdms *.rtdc)')
        if pathlist:
            # add to list
            self.append_paths(pathlist)

    def on_change_sample_names(self):
        """Update the sample names of the datasets"""
        invalid = []
        for row in range(self.tableWidget.rowCount()):
            path_index = int(self.tableWidget.item(row, 0).text())
            path = self.pathlist[path_index]
            newname = self.tableWidget.item(row, 2).text()
            oldname = meta_tool.get_sample_name(path)
            if isinstance(oldname, bytes):
                oldname = oldname.decode('utf_8')
            # compare sample names bytes-insensitive
            if newname != oldname:
                if path.suffix == ".tdms":
                    # not supported for tdms files
                    invalid.append(path)
                else:
                    # change sample name
                    with h5py.File(path, "a") as h5:
                        h5.attrs["experiment:sample"] = np.string_(
                            newname.encode("utf-8"))
                    # add entry to the log
                    task_dict = {
                        "name": "update attributes",
                        "old": {"experiment:sample": oldname},
                        "new": {"experiment:sample": newname},
                        }
                    append_execution_log(path, task_dict)
        if invalid:
            raise ValueError("Changing the sample name for .tdms files is "
                             + "not supported! Please convert the files to "
                             + "the .rtdc file format. Affected files are:\n"
                             + "\n".join([str(p) for p in invalid]))

    def on_clear_measurements(self):
        """Clear the table"""
        for _ in range(len(self.pathlist)):
            self.tableWidget.removeRow(0)
        self.pathlist = []

    def on_join(self):
        """Join multiple RT-DC measurements"""
        pass

    def on_table_text_changed(self):
        """Reset sample name if set to empty string"""
        curit = self.tableWidget.currentItem()
        if curit is not None and curit.text() == "":
            row = self.tableWidget.currentRow()
            path_index = int(self.tableWidget.item(row, 0).text())
            sample = meta_tool.get_sample_name(self.pathlist[path_index])
            if isinstance(sample, bytes):
                sample = sample.decode("utf-8")
            self.tableWidget.item(row, 2).setText(sample)

    def on_tdms2rtdc(self):
        """Convert .tdms files to .rtdc files"""
        pass


def append_execution_log(path, task_dict):
    info = get_job_info()
    info["libraries"]["shapeout"] = soversion
    info["task"] = task_dict
    history.append_history(path, info)


def excepthook(etype, value, trace):
    """
    Handler for all unhandled exceptions.

    :param `etype`: the exception type (`SyntaxError`,
        `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it
        prints the standard Python header: ``Traceback (most recent
        call last)``.
    """
    vinfo = "Unhandled exception in Shape-Out version {}:\n".format(
        __version__)
    tmp = traceback.format_exception(etype, value, trace)
    exception = "".join([vinfo]+tmp)

    errorbox = QtWidgets.QMessageBox()
    errorbox.addButton(QtWidgets.QPushButton('Close'),
                       QtWidgets.QMessageBox.YesRole)
    errorbox.addButton(QtWidgets.QPushButton(
        'Copy text && Close'), QtWidgets.QMessageBox.NoRole)
    errorbox.setText(exception)
    ret = errorbox.exec_()
    if ret == 1:
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(exception)


# Make Ctr+C close the app
signal.signal(signal.SIGINT, signal.SIG_DFL)
# Display exception hook in separate dialog instead of crashing
sys.excepthook = excepthook
