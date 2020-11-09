from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import mgear.menu
import mgear
import pymel.core as pm


def install():
    """Install Skinning submenu
    """
    pm.setParent(mgear.menu_id, menu=True)
    pm.menuItem(divider=True)
    commands = (
        ("Anim Picker", str_open_picker_mode),
        ("-----", None),
        ("Edit Anim Picker", str_open_edit_mode)
    )

    mgear.menu.install("Anim Picker", commands)


str_open_picker_mode = """
from mgear import anim_picker
anim_picker.load(False, False)
"""

str_open_edit_mode = """
from mgear import anim_picker
anim_picker.load(True, False)
"""
