import pkg_resources

import dclab
from dclab.rtdc_dataset import feat_temp
from PyQt5 import uic, QtCore, QtWidgets

from . import dlg_icheck


class Preferences(QtWidgets.QDialog):
    """Preferences dialog to interact with QSettings"""
    instances = {}
    feature_changed = QtCore.pyqtSignal()

    def __init__(self, parent, *args, **kwargs):
        QtWidgets.QWidget.__init__(self, parent=parent, *args, **kwargs)
        path_ui = pkg_resources.resource_filename("dckit", "preferences.ui")
        uic.loadUi(path_ui, self)
        self.settings = QtCore.QSettings()
        self.parent = parent

        #: configuration keys, corresponding widgets, and defaults
        self.config_pairs = [
            ["check for updates", self.general_check_for_updates, "1"],
            # comma-separated list of features
            ["included features", self.listWidget_features, ""],
        ]

        self.reload()

        # signals
        # features
        self.pushButton_add_feature.clicked.connect(self.on_feature_add)
        self.pushButton_remove_features.clicked.connect(self.on_feature_rm)
        # dialog
        self.btn_apply = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Apply)
        self.btn_apply.clicked.connect(self.on_settings_apply)
        self.btn_cancel = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.Cancel)
        self.btn_ok = self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
        self.btn_ok.clicked.connect(self.on_settings_apply)
        self.btn_restore = self.buttonBox.button(
            QtWidgets.QDialogButtonBox.RestoreDefaults)
        self.btn_restore.clicked.connect(self.on_settings_restore)

    @QtCore.pyqtSlot()
    def on_feature_add(self, feat=None, scalar=None):
        """User adds a new feature"""
        if feat is None:
            # open a dialog where the user can enter text
            feat, ok_pressed = QtWidgets.QInputDialog.getText(
                self,
                "Add new feature",
                "Please enter the feature name",
            )
        else:
            ok_pressed = True
        feat = feat.strip()
        if ok_pressed and feat:
            # ask the user whether this is a scalar feature
            if scalar is None:
                reply = QtWidgets.QMessageBox.question(
                    self,
                    "Register as scalar feature?",
                    f"Is '{feat}' a scalar feature (one scalar value per "
                    + "event as e.g. for deformation)?"
                )
                scalar = reply == QtWidgets.QMessageBox.Yes
            feat = feat.strip()
            item = QtWidgets.QListWidgetItem(
                f"{feat} " + ("(scalar)" if scalar else "(non-scalar)"),
            )
            self.listWidget_features.insertItem(-1, item)
            item.setData(100, feat)
            item.setData(101, scalar)

    @QtCore.pyqtSlot()
    def on_feature_rm(self):
        """User removes one or more features"""
        selected = self.listWidget_features.selectedItems()
        for row in range(self.listWidget_features.count()):
            if self.listWidget_features.item(row) in selected:
                self.listWidget_features.takeItem(row)

    def reload(self):
        """Read configuration or set default parameters"""
        for key, widget, default in self.config_pairs:
            value = self.settings.value(key, default)
            if isinstance(widget, QtWidgets.QCheckBox):
                widget.setChecked(bool(int(value)))
            elif isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(value)
            elif widget is self.listWidget_features:
                # comma-separated list
                widget.clear()
                for feat in value.split(","):
                    scalar = bool(int(self.settings.value(
                        f"feature scalar {feat}", "0")))
                    self.on_feature_add(feat=feat, scalar=scalar)
            else:
                raise NotImplementedError("No rule for '{}'".format(key))
        register_temporary_features()

    @QtCore.pyqtSlot()
    def on_settings_apply(self):
        """Save current changes made in UI to settings and reload UI"""
        for key, widget, default in self.config_pairs:
            if isinstance(widget, QtWidgets.QCheckBox):
                value = int(widget.isChecked())
            elif isinstance(widget, QtWidgets.QLineEdit):
                value = widget.text().strip()
            elif widget is self.listWidget_features:
                # comma-separated list
                features = []
                for row in range(widget.count()):
                    item = widget.item(row)
                    feat = item.data(100)
                    features.append(feat)
                    # also write scalarness
                    self.settings.setValue(f"feature scalar {feat}",
                                           str(int(item.data(101))))
                value = ",".join(sorted(set(features)))
            else:
                raise NotImplementedError("No rule for '{}'".format(key))
            self.settings.setValue(key, value)

        # reload UI to give visual feedback
        self.reload()

    @QtCore.pyqtSlot()
    def on_settings_restore(self):
        self.settings.clear()
        self.reload()


def register_temporary_features():
    """Register all temporary features in the QSettings"""
    settings = QtCore.QSettings()
    fdata = settings.value("included features", "").strip()
    feat_temp.deregister_all()
    if fdata:
        for feat in fdata.split(","):
            if feat and not dclab.dfn.feature_exists(feat):
                scalar = bool(int(settings.value(
                    f"feature scalar {feat}")))
                feat_temp.register_temporary_feature(feat, is_scalar=scalar)
    # Clear the check_dataset cache otherwise any new feature will be
    # shown as unknown.
    dlg_icheck.check_dataset.cache_clear()
