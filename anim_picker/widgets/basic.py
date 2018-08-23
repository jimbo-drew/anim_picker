# python
import os

# dcc
import maya.cmds as cmds

# mgear
from mgear.synoptic import utils
from mgear.vendor.Qt import QtCore, QtWidgets, QtGui

# module
from anim_picker.handlers import __EDIT_MODE__

# seems to conflicts with maya viewports...
__USE_OPENGL__ = True

DEFAULTS_SPACES_ = {"Arm": {"Shoulder": ["armUI_L0_ctl",
                                         "shoulder_rotRef",
                                         "armUI_R0_ctl",
                                         "shoulder_rotRef"],
                            "IK Pos": ["armUI_L0_ctl",
                                       "arm_ikref",
                                       "armUI_R0_ctl",
                                       "arm_ikref"],
                            "IK Rot": ["armUI_L0_ctl",
                                       "arm_ikRotRef",
                                       "armUI_R0_ctl",
                                       "arm_ikRotRef"],
                            "Up Vector": ["armUI_L0_ctl",
                                          "arm_upvref",
                                          "armUI_R0_ctl",
                                          "arm_upvref"]},
                    "Head": ["spineUI_C0_ctl", "neck_ikref"],
                    "Leg": {"IK Pos": ["legUI_L0_ctl",
                                       "leg_ikref",
                                       "legUI_R0_ctl",
                                       "leg_ikref"],
                            "Up Vector": ["legUI_L0_ctl",
                                          "leg_upvref",
                                          "legUI_R0_ctl",
                                          "leg_upvref"]}}


# =============================================================================
# generic functions
# =============================================================================
def get_module_path():
    '''Return the folder path for this module
    '''
    return os.path.dirname(os.path.abspath(__file__))


def get_images_folder_path():
    '''Return path for package images folder
    '''
    # Get the path to this file
    module_path = os.path.dirname(get_module_path())
    return os.path.join(module_path, "images")


# SpaceSwitcher is intended to be a temporary addition of spaces --------------
class SpaceSwitcher(QtWidgets.QWidget):
    """temporary replacement for the space switcher in synoptic"""
    def __init__(self, parent=None):
        super(SpaceSwitcher, self).__init__(parent=parent)
        self.spaces_dict = {}
        #  --------------------------------------------------------------------
        self.setFixedHeight(120)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        # self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(2, 1, 2, 1)
        # space optionbs ------------------------------------------------------
        self.space_widget = None

    def set_tab_widget(self, tab_widget):
        self.tab_widget = tab_widget
        self.tab_widget.currentChanged.connect(self.update)

    def setToEdit(self, state=False):
        for box in self.space_box:
            box.edit_mode = state

    def update(self, index, space_dict=DEFAULTS_SPACES_):
        if index == -1:
            try:
                self.space_widget.close()
                self.space_widget.deleteLater()
            except Exception:
                pass
            self.space_widget = None
            return
        gView = self.tab_widget.widget(index)
        self.set_data(gView, space_dict)

    def set_data(self, scene, spaces_dict):
        self.scene = scene
        self.spaces_dict = spaces_dict
        if self.space_widget is not None:
            # self.space_widget.close()
            self.space_widget.deleteLater()
        self.create_space_widget()

    def create_space_widget(self):
        self.space_widget = QtWidgets.QWidget()
        space_Layout = QtWidgets.QHBoxLayout()
        space_Layout.setContentsMargins(0, 0, 0, 0)
        self.space_widget.setLayout(space_Layout)
        space_Layout.addLayout(self.arm_column(), 1)
        right_layout = QtWidgets.QVBoxLayout()
        right_layout.addLayout(self.head_column(), 1)
        right_layout.addLayout(self.leg_column(), 1)
        space_Layout.addLayout(right_layout, 1)
        self.main_layout.addWidget(self.space_widget)

    def double_spaceRow(self, ctrl_a, attr_a, label, ctrl_b, attr_b):
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignHCenter)
        combo_a = SpaceComboBox(self.scene.namespace, ctrl_a, attr_a)
        combo_a.setMinimumWidth(60)
        row_label = QtWidgets.QLabel(label)
        row_label.setMinimumWidth(60)
        combo_b = SpaceComboBox(self.scene.namespace, ctrl_b, attr_b)
        combo_b.setMinimumWidth(60)
        layout.addWidget(combo_a)
        layout.addWidget(row_label)
        layout.addWidget(combo_b)
        return layout

    def leg_column(self):
        leg_layout = QtWidgets.QVBoxLayout()
        leg_label = QtWidgets.QLabel("Leg")
        leg_layout.addWidget(leg_label)

        for label, row_list in self.spaces_dict["Leg"].iteritems():
            ctrl_a, attr_a, ctrl_b, attr_b = row_list
            space_row = self.double_spaceRow(ctrl_a,
                                             attr_a,
                                             label,
                                             ctrl_b,
                                             attr_b)
            leg_layout.addLayout(space_row, 1)
        return leg_layout

    def head_column(self):
        head_layout = QtWidgets.QVBoxLayout()
        head_label = QtWidgets.QLabel("Head")
        head_layout.addWidget(head_label, 1)
        row_list = self.spaces_dict["Head"]
        space_row = SpaceComboBox(self.scene.namespace,
                                  row_list[0],
                                  row_list[1])
        head_layout.addWidget(space_row, 1)
        return head_layout

    def arm_column(self):
        arm_layout = QtWidgets.QVBoxLayout()
        arm_label = QtWidgets.QLabel("Arm")
        arm_layout.addWidget(arm_label)

        for label, row_list in self.spaces_dict["Arm"].iteritems():
            ctrl_a, attr_a, ctrl_b, attr_b = row_list
            space_row = self.double_spaceRow(ctrl_a,
                                             attr_a,
                                             label,
                                             ctrl_b,
                                             attr_b)
            arm_layout.addLayout(space_row, 1)
        return arm_layout


# SpaceComboBox should be able to stay, will need refinement ------------------
class SpaceComboBox(QtWidgets.QComboBox):
    """space switching toggle"""
    def __init__(self, namespace, ctrl_name, combo_attr, parent=None):
        super(SpaceComboBox, self).__init__(parent=parent)
        if namespace == "" or namespace is None:
            self.namespace = ""
        else:
            self.namespace = "{}:".format(namespace)
        self.ctrl_name = ctrl_name
        self.combo_attr = combo_attr
        self.refresh()
        self.currentIndexChanged.connect(self.spaceChanged)

    def muteSignals(func):
        def wrapper(self, *args):
            self.blockSignals(True)
            try:
                func(self, *args)
            except Exception:
                pass
            self.blockSignals(False)
            return
        return wrapper

    @muteSignals
    def refresh(self):
        self.clear()
        spaces = utils.getComboKeys(self.namespace,
                                    self.ctrl_name,
                                    self.combo_attr)
        self.addItems(spaces)

        self.setCurrentIndex(utils.getComboIndex(self.namespace,
                                                 self.ctrl_name,
                                                 self.combo_attr))

    def enterEvent(self, event):
        super(SpaceComboBox, self).enterEvent(event)
        self.refresh()

    @muteSignals
    def spaceChanged(self, index):
        if __EDIT_MODE__.get():
            return
        if self.currentIndex() == self.count() - 1:
            utils.ParentSpaceTransfer.showUI(self,
                                             self.namespace,
                                             self.ctrl_name,
                                             self.ctrl_name,
                                             self.ctrl_name)
        else:
            utils.changeSpace(self.namespace,
                              self.ctrl_name,
                              self.combo_attr,
                              self.currentIndex(),
                              self.ctrl_name)


def promptAcceptance(parent, descriptionA, descriptionB):
    """Warn user, asking for permission

    Args:
        parent (QWidget): to be parented under
        descriptionA (str): info
        descriptionB (str): further info

    Returns:
        QtCore.Response: accept, deline, reject
    """
    msgBox = QtWidgets.QMessageBox(parent)
    msgBox.setText(descriptionA)
    msgBox.setInformativeText(descriptionB)
    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok |
                              QtWidgets.QMessageBox.Cancel)
    msgBox.setDefaultButton(QtWidgets.QMessageBox.Cancel)
    decision = msgBox.exec_()
    return decision


# =============================================================================
# Custom Widgets ---
# =============================================================================
class CallbackButton(QtWidgets.QPushButton):
    '''Dynamic callback button
    '''

    def __init__(self, callback=None, *args, **kwargs):
        QtWidgets.QPushButton.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        # Connect event
        self.clicked.connect(self.click_event)

        # Set tooltip
        if hasattr(self.callback, "__doc__") and self.callback.__doc__:
            self.setToolTip(self.callback.__doc__)

    def click_event(self):
        if not self.callback:
            return
        self.callback(*self.args, **self.kwargs)


class CallbackComboBox(QtWidgets.QComboBox):
    '''Dynamic combo box object
    '''

    def __init__(self, callback=None, status_tip=None, *args, **kwargs):
        QtWidgets.QComboBox.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        if status_tip:
            self.setStatusTip(status_tip)

        self.currentIndexChanged.connect(self.index_change_event)

    def index_change_event(self, index):
        if not self.callback:
            return
        self.callback(index=index, *self.args, **self.kwargs)


class CallBackSpinBox(QtWidgets.QSpinBox):
    def __init__(self, callback, value=0, min=0, max=9999, *args, **kwargs):
        QtWidgets.QSpinBox.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        # Set properties
        self.setRange(min, max)
        self.setValue(value)

        # Signals
        self.valueChanged.connect(self.valueChangedEvent)

    def valueChangedEvent(self, value):
        if not self.callback:
            return
        self.callback(value=value, *self.args, **self.kwargs)


class CallBackDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, callback, value=0, min=0, max=9999, *args, **kwargs):
        QtWidgets.QDoubleSpinBox.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        # Set properties
        self.setRange(min, max)
        self.setValue(value)

        # Signals
        self.valueChanged.connect(self.valueChangedEvent)

    def valueChangedEvent(self, value):
        if not self.callback:
            return
        self.callback(value=value, *self.args, **self.kwargs)


class CallbackLineEdit(QtWidgets.QLineEdit):
    def __init__(self, callback, text=None, *args, **kwargs):
        QtWidgets.QLineEdit.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        # Set properties
        if text:
            self.setText(text)

        # Signals
        self.returnPressed.connect(self.return_pressed_event)

    def return_pressed_event(self):
        '''Will return text on return press
        '''
        self.callback(text=self.text(), *self.args, **self.kwargs)


class CallbackListWidget(QtWidgets.QListWidget):
    '''Dynamic List Widget object
    '''

    def __init__(self, callback=None, *args, **kwargs):
        QtWidgets.QListWidget.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        self.itemDoubleClicked.connect(self.double_click_event)

        # Set selection mode to multi
        self.setSelectionMode(self.ExtendedSelection)

    def double_click_event(self, item):
        if not self.callback:
            return
        self.callback(item=item, *self.args, **self.kwargs)


class CallbackCheckBoxWidget(QtWidgets.QCheckBox):
    '''Dynamic CheckBox Widget object
    '''

    def __init__(self,
                 callback=None,
                 value=False,
                 label=None,
                 *args,
                 **kwargs):
        QtWidgets.QCheckBox.__init__(self)
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

        # Set init state
        if value:
            self.setCheckState(QtCore.Qt.Checked)
        self.setText(label or "")

        self.toggled.connect(self.toggled_event)

    def toggled_event(self, value):
        if not self.callback:
            return
        self.kwargs["value"] = value
        self.callback(*self.args, **self.kwargs)


class CallbackRadioButtonWidget(QtWidgets.QRadioButton):
    '''Dynamic callback radioButton
    '''

    def __init__(self, name_value, callback, checked=False):
        QtWidgets.QRadioButton.__init__(self)
        self.name_value = name_value
        self.callback = callback

        self.setChecked(checked)

        self.clicked.connect(self.click_event)

    def click_event(self):
        self.callback(self.name_value)


class CtrlListWidgetItem(QtWidgets.QListWidgetItem):
    '''
    List widget item for influence list
    will handle checks, color feedbacks and edits
    '''

    def __init__(self, index=0, text=None):
        QtWidgets.QListWidgetItem.__init__(self)

        self.index = index
        if text:
            self.setText(text)

    def setText(self, text):
        '''Overwrite default setText with auto color status check
        '''
        # Skip if name hasn't changed
        if text == self.text():
            return None

        # Run default setText action
        QtWidgets.QListWidgetItem.setText(self, text)

        # Set color status
        self.set_color_status()

        return text

    def node(self):
        '''Return a usable string for maya instead of a QString
        '''
        return unicode(self.text())

    def node_exists(self):
        '''Will check that the node from "text" exists
        '''
        return cmds.objExists(self.node())

    def set_color_status(self):
        '''Set the color to red/green based on node existence status
        '''
        color = QtGui.QColor()

        # Exists case
        if self.node_exists():
            # pale green
            color.setRgb(152, 251, 152)

        # Does not exists case
        else:
            # orange
            color.setRgb(255, 165, 0)

        brush = self.foreground()
        brush.setColor(color)
        self.setForeground(brush)


class BackgroundWidget(QtWidgets.QLabel):
    '''QLabel widget to support background options for tabs.
    '''

    def __init__(self,
                 parent=None):
        QtWidgets.QLabel.__init__(self, parent)

        self.setBackgroundRole(QtGui.QPalette.Base)
        self.background = None

    def _assert_path(self, path):
        assert os.path.exists(path), "Could not find file {}".format(path)

    def resizeEvent(self, event):
        QtWidgets.QLabel.resizeEvent(self, event)
        self._set_stylesheet_background()

    def _set_stylesheet_background(self):
        '''
        Will set proper sylesheet based on edit status to have
        fixed size background in edit mode and stretchable in anim mode
        '''
        if not self.background:
            self.setStyleSheet("")
            return

        bg = self.background
        if __EDIT_MODE__.get():
            edit_css = "QLabel {background-image: url('{}'); background-repeat: no repeat;}".format(bg)
            self.setStyleSheet(edit_css)
        else:
            self.setStyleSheet("QLabel {border-image: url('{}');}".format(bg))

    def set_background(self, path=None):
        '''Set character snapshot picture
        '''
        if not (path and os.path.exists(path)):
            path = None
            self.background = None
        else:
            self.background = unicode(path)

        # Use stylesheet rather than pixmap for proper resizing support
        self._set_stylesheet_background()

    def file_dialog(self):
        '''Get file dialog window starting in default folder
        '''
        imgs_dir = get_images_folder_path()
        file_path = QtWidgets.QFileDialog.getOpenFileName(self,
                                                          'Choose picture',
                                                          imgs_dir)
        # Filter return result (based on qt version)
        if isinstance(file_path, tuple):
            file_path = file_path[0]

        if not file_path:
            return

        return file_path


class SnapshotWidget(BackgroundWidget):
    '''Top right character "snapshot" widget, to display character picture
    '''

    def __init__(self, parent=None):
        BackgroundWidget.__init__(self, parent)

        self.setFixedWidth(80)
        self.setFixedHeight(80)

        self.set_background()

        self.setToolTip("Click here to Open About/Help window")

    def _get_default_snapshot(self, name="undefined"):
        '''Return default snapshot
        '''
        # Define image path
        folder_path = get_images_folder_path()
        image_path = os.path.join(folder_path, "{}.png".format(name))

        # Assert path
        self._assert_path(image_path)

        return image_path

    def set_background(self, path=None):
        '''Set character snapshot picture
        '''
        if not (path and os.path.exists(path)):
            path = self._get_default_snapshot()
            self.background = None
        else:
            self.background = path

        # Load image
        image = QtGui.QImage(path)
        self.setPixmap(QtGui.QPixmap.fromImage(image))

    def contextMenuEvent(self, event):
        '''Right click menu options
        '''
        # Abort in non edit mode
        if not __EDIT_MODE__.get():
            return

        # Init context menu
        menu = QtWidgets.QMenu(self)

        # Add choose action
        choose_action = QtWidgets.QAction("Select Picture", None)
        choose_action.triggered.connect(self.select_image)
        menu.addAction(choose_action)

        # Add reset action
        reset_action = QtWidgets.QAction("Reset", None)
        reset_action.triggered.connect(self.reset_image)
        menu.addAction(reset_action)

        # Open context menu under mouse
        if not menu.isEmpty():
            menu.exec_(self.mapToGlobal(event.pos()))

    def select_image(self):
        '''Pick/set snapshot image
        '''
        # Open file dialog
        file_name = self.file_dialog()

        # Abort on cancel
        if not file_name:
            return

        # Set picture
        self.set_background(file_name)

    def reset_image(self):
        '''Reset snapshot image to default
        '''
        # Reset background
        self.set_background()

    def get_data(self):
        '''Return snapshot picture path
        '''
        return self.background
