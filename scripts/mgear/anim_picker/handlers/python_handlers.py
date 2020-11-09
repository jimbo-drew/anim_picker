from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# Copyright (c) 2018 Guillaume Barlier
# This file is part of "anim_picker" and covered by MIT,
# read LICENSE.md and COPYING.md for details.

import pprint


def safe_code_exec(cmd, env=None):
    '''Safely execute code in new namespace with specified dictionary
    '''
    if env is None:
        env = {}
    try:
        exec(cmd, env)
    except Exception as e:
        pprint.pprint(e)
