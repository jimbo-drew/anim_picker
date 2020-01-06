import mgear.menu
from mgear import anim_picker
from functools import partial


def install():
    """Install Skinning submenu
    """
    commands = (
        ("Anim Picker", partial(anim_picker.load, edit=False)),
        ("-----", None),
        ("Edit Anim Picker", partial(anim_picker.load, edit=True))
    )

    mgear.menu.install("Anim Picker", commands)
