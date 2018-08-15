# Copyright (c) 2018 Guillaume Barlier
# This file is part of "anim_picker" and covered by MIT,
# read LICENSE.md and COPYING.md for details.
import gui
reload(gui)

__version__ = "1.0.4"


def load(edit=False, dockable=True):
    '''Fast load method
    '''
    return gui.load(edit=edit, dockable=dockable)
