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


"""
Search TODO, FIXME and similar comments in project files.
"""


###############################################################################
####

import sys
from . import todos
from . import exceptions


###############################################################################
####

if __name__ == '__main__':
    try:
        TODOS = todos.Todos()
        TODOS.main(sys.argv[1:])
    except KeyboardInterrupt as keyboard_exception:
        sys.exit('ERROR: Interrupted by user')
    except exceptions.TodosFatalError as todos_exception:
        sys.exit('FATAL ERROR: {0}'.format(todos_exception.value))
