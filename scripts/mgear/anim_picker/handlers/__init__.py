from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# Copyright (c) 2018 Guillaume Barlier
# This file is part of "anim_picker" and covered by MIT,
# read LICENSE.md and COPYING.md for details.

from . import mode_handlers
from . import maya_handlers

# INIT HANDLERS INSTANCES
__EDIT_MODE__ = mode_handlers.EditMode()
__SELECTION__ = maya_handlers.SelectionCheck()
