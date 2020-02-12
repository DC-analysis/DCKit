import json
import functools
import pkg_resources

import dclab
from PyQt5 import uic, QtWidgets
from dclab.rtdc_dataset.check import VALID_CHOICES


class IntegrityCheckDialog(QtWidgets.QDialog):
    #: Remembers user-defined metadata
    user_metadata = {}

    def __init__(self, parent, path, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, parent, *args, **kwargs)
        path_ui = pkg_resources.resource_filename("dckit", "dlg_icheck.ui")
        uic.loadUi(path_ui, self)

        self.path = path
        #: metadata (remember across instances)
        if self.path not in IntegrityCheckDialog.user_metadata:
            IntegrityCheckDialog.user_metadata[self.path] = {}
        self.metadata = IntegrityCheckDialog.user_metadata[self.path]
        #: return state ("unchecked", "passed", "incomplete", "tolerable")
        self.state = "unchecked"

        # check and fill data
        self.populate_ui()

    def populate_ui(self):
        """Run check and set missing UI elements"""
        # perform initial check
        cues = self.check(use_metadata=False)
        # Fill in user-changeable things
        miss_count = 0
        wrong_count = 0
        self.user_widgets = {}
        for cue in cues:
            if cue.category in ["metadata missing", "metadata wrong"]:
                # label
                sec = cue.cfg_section
                key = cue.cfg_key
                lab = QtWidgets.QLabel("[{}]: {}".format(sec, key))
                lab.setToolTip(dclab.dfn.config_descr[sec][key])
                if cue.level == "violation":
                    lab.setStyleSheet('color: #A50000')
                else:
                    lab.setStyleSheet('color: #7A6500')
                if cue.category == "metadata missing":
                    self.gridLayout_missing.addWidget(lab, miss_count, 0)
                else:
                    self.gridLayout_wrong.addWidget(lab, wrong_count, 0)
                # control
                if cue.cfg_choices is None:
                    dt = dclab.dfn.config_types[cue.cfg_section][cue.cfg_key]
                    if dt is str:
                        wid = QtWidgets.QLineEdit(self)
                        wid.setText(self.get_metadata_value(sec, key) or "")
                    elif dt is float:
                        wid = QtWidgets.QDoubleSpinBox(self)
                        wid.setMinimum(-1337)
                        wid.setMaximum(999999999)
                        wid.setDecimals(5)
                        value = self.get_metadata_value(sec, key) or -1337
                        wid.setValue(value)
                    elif dt is int:
                        wid = QtWidgets.QSpinBox(self)
                        wid.setMinimum(-1337)
                        wid.setMaximum(999999999)
                        value = self.get_metadata_value(sec, key) or -1337
                        wid.setValue(value)
                    elif dt is bool:
                        wid = QtWidgets.QComboBox(self)
                        wid.addItem("Please select", None)
                        wid.addItem("True", True)
                        wid.addItem("False", False)
                        idx = wid.findData(self.get_metadata_value(sec, key))
                        wid.setCurrentIndex(idx)
                    else:
                        raise ValueError("No action specified '{}'".format(dt))
                else:
                    wid = QtWidgets.QComboBox(self)
                    wid.addItem("Please select", None)
                    for item in VALID_CHOICES[sec][key]:
                        wid.addItem(item, item)
                    idx = wid.findData(self.get_metadata_value(sec, key))
                    wid.setCurrentIndex(idx)
                if cue.category == "metadata missing":
                    self.gridLayout_missing.addWidget(wid, miss_count, 1)
                    miss_count += 1
                else:
                    self.gridLayout_wrong.addWidget(wid, wrong_count, 1)
                    wrong_count += 1
                # remember all widgets for saving metadata later
                if sec not in self.user_widgets:
                    self.user_widgets[sec] = {}
                self.user_widgets[sec][key] = wid
        if not miss_count:
            self.groupBox_missing.hide()
        if not wrong_count:
            self.groupBox_wrong.hide()
        # Show complete log
        cues2 = self.check(use_metadata=True, expand_section=False)
        text = ""
        colors = {"info": "k",
                  "alert": "#7A6500",
                  "violation": "#A50000"}
        for cue in cues2:
            text += "<div style='color:{}'>{}</div>".format(colors[cue.level],
                                                            cue.msg)
        self.textEdit.setText(text)

        # Logs
        with dclab.new_dataset(self.path) as ds:
            if ds.logs:
                for log in ds.logs:
                    self.comboBox_logs.addItem(log, log)
            else:
                self.widget_logs.hide()
            self.comboBox_logs.currentIndexChanged.connect(self.on_logs)

    def check(self, use_metadata=True, expand_section=True):
        if use_metadata:
            metadata_dump = json.dumps(self.metadata, sort_keys=True)
        else:
            metadata_dump = json.dumps({})
        cues = check_dataset(self.path, metadata_dump, expand_section)
        return cues

    def done(self, r):
        if r:
            # save metadata
            self.save_current_metadata()
        # run check again
        cues = self.check()
        levels = dclab.rtdc_dataset.check.ICue.get_level_summary(cues)
        if levels["violation"]:
            self.state = "failed"
        elif levels["alert"]:
            self.state = "tolerable"
        else:
            self.state = "passed"

        super(IntegrityCheckDialog, self).done(r)

    def get_metadata_value(self, section, key):
        value = None
        if section in self.metadata:
            if key in self.metadata[section]:
                value = self.metadata[section][key]
        return value

    def on_logs(self):
        log = self.comboBox_logs.currentData()
        if log is None:
            return
        dlg = QtWidgets.QDialog()
        dlg.setWindowTitle("{}: {}".format(self.path.name, log))
        path_ui = pkg_resources.resource_filename("dckit", "dlg_log.ui")
        uic.loadUi(path_ui, dlg)
        dlg.label.setText(log)
        with dclab.new_dataset(self.path) as ds:
            text = "\n".join(ds.logs[log])
            dlg.plainTextEdit.setPlainText(text)
        dlg.exec_()

    def save_current_metadata(self):
        for sec in self.user_widgets:
            for key in self.user_widgets[sec]:
                wid = self.user_widgets[sec][key]
                if isinstance(wid, QtWidgets.QComboBox):
                    value = wid.currentData()
                elif isinstance(wid, (QtWidgets.QSpinBox,
                                      QtWidgets.QDoubleSpinBox)):
                    value = wid.value()
                else:
                    value = wid.text()
                if value is not None and value and value != -1337:
                    if sec not in self.metadata:
                        self.metadata[sec] = {}
                    self.metadata[sec][key] = value


@functools.lru_cache(maxsize=1000)
def check_dataset(path, metadata_dump, expand_section):
    """Caching wrapper for integrity checks"""
    metadata = json.loads(metadata_dump)
    with dclab.new_dataset(path) as ds:
        ds.config.update(metadata)
        ic = dclab.rtdc_dataset.check.IntegrityChecker(ds)
        cues = ic.check(expand_section=expand_section)
    return cues
