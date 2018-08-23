# Copyright (c) 2018 Guillaume Barlier
# This file is part of "anim_picker" and covered by MIT,
# read LICENSE.md and COPYING.md for details.

import os
import json

from mgear.core import pyqt
from mgear.vendor.Qt import QtWidgets

from anim_picker.widgets import basic


# i/o -------------------------------------------------------------------------
def _importData(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            return data
    except Exception as e:
        print e


def _exportData(data, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, sort_keys=False, indent=4)
    except Exception as e:
        print e


def read_data_file(file_path):
    '''Read data from file
    '''
    msg = "{} does not seem to be a file".format(file_path)
    assert os.path.isfile(file_path), msg
    pkr_data = _importData(file_path) or {}
    return pkr_data


def write_data_file(file_path, data={}, force=False):
    '''Write data to file

    # kwargs:
    file_path: the file path to write to
    data: the data to write
    f (bool): force write mode, if false, will ask for confirmation when
    overwriting existing files
    '''
    # Ask for confirmation on existing file
    if os.path.exists(file_path) and not force:
        decision = basic.promptAcceptance(pyqt.maya_main_window(),
                                          "File already exists! Overwrite?",
                                          "YOU SURE?")
        if decision in [QtWidgets.QMessageBox.Discard,
                        QtWidgets.QMessageBox.Cancel]:
            return

    # write file
    _exportData(data, file_path)
