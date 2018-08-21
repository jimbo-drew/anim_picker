from Qt import QtWidgets, QtCore

from mgear.synoptic import utils

from anim_picker.handlers import __EDIT_MODE__

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
