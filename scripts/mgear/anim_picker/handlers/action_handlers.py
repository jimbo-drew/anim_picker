

# TODO: Synoptic utils should be refactor in mgear_core or in anim_picker.
# we should not be depend of synoptic package
from mgear.synoptic import utils

from mgear.vendor.Qt import QtCore, QtWidgets, QtGui


def get_instance(parent, gui_class):
    for children in parent.children():
        if isinstance(children, gui_class):
            return children
    return None


class DropListMenu(QtWidgets.QMenu):

    def __init__(self,
                 namespace,
                 ui_host,
                 combo_attr,
                 ctl,
                 self_widget,
                 *args,
                 **kwargs):
        super(DropListMenu, self).__init__(*args, **kwargs)
        self.namespace = namespace
        self.ui_host = ui_host
        self.combo_attr = combo_attr
        self.ctl = ctl
        self.self_widget = self_widget

        self.init_gui()

    def init_gui(self):
        self.listWidget = QtWidgets.QListWidget(self)
        action = QtWidgets.QWidgetAction(self)
        action.setDefaultWidget(self.listWidget)
        self.addAction(action)
        self.listWidget.setFocus()

        self.list1 = utils.getComboKeys(
            self.namespace, self.ui_host, self.combo_attr)
        self.listWidget.addItems(self.list1)
        current_idx = utils.getComboIndex(
            self.namespace, self.ui_host, self.combo_attr)
        self.listWidget.setCurrentRow(current_idx)

        self.listWidget.currentRowChanged.connect(self.accept)

    def accept(self):

        if self.listWidget.currentRow() == self.listWidget.count() - 1:
            self.listWidget.setCurrentRow(utils.getComboIndex(
                self.namespace, self.ui_host, self.combo_attr))
            utils.ParentSpaceTransfer.showUI(self.listWidget,
                                             self.namespace,
                                             self.ui_host,
                                             self.combo_attr,
                                             self.ctl)
        else:

            utils.changeSpace(self.namespace,
                              self.ui_host,
                              self.combo_attr,
                              self.listWidget.currentRow(),
                              self.ctl)
            space = self.listWidget.item(self.listWidget.currentRow()).text()
            self.self_widget.text.set_text(space)
        self.close()
        self.deleteLater()


def get_main_window(widget=None):
    widget = widget or QtWidgets.QApplication.activeWindow()
    if widget is None:
        return
    parent = widget.parent()
    if parent is None:
        return widget
    return get_main_window(parent)


def position_window(window):
    pos = QtGui.QCursor.pos()
    window.move(pos.x(), pos.y())


def show_drop_list(namespace,
                   ui_host,
                   combo_attr,
                   ctl,
                   self_widget,
                   env_init):

    if env_init:
        list1 = utils.getComboKeys(
            namespace, ui_host, combo_attr)
        current_idx = utils.getComboIndex(
            namespace, ui_host, combo_attr)
        self_widget.text.set_text(list1[current_idx])

    else:
        maya_window = get_main_window()
        # look for existing instances of QuickLauncher
        ql = get_instance(maya_window, DropListMenu)
        if ql:
            ql.deleteLater()
        # create a new instance
        ql = DropListMenu(namespace,
                          ui_host,
                          combo_attr,
                          ctl,
                          self_widget,
                          maya_window)

        position_window(ql)
        ql.exec_()

