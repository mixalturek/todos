#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2013 Michal Turek
#
# This file is part of TODOs.
# http://todos.sourceforge.net/
#
# TODOs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# TODOs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TODOs.  If not, see <http://www.gnu.org/licenses/>.
#


# Execute with
# $ python todos/__main__.py (2.6+)
# $ python -m todos          (2.7+)

"""
Search TODO, FIXME and similar comments in project files.
"""

import sys
import todos.todos


if __package__ is None and not hasattr(sys, "frozen"):
    # direct call of __main__.py
    import os.path
    PATH = os.path.realpath(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(os.path.dirname(PATH)))


if __name__ == '__main__':
    try:
        TODOS = todos.todos.Todos()
        TODOS.main(sys.argv[1:])
    except KeyboardInterrupt as keyboard_exception:
        sys.exit('\nERROR: Interrupted by user')
