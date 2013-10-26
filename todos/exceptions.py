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
Exception classes.
"""


###############################################################################
####

class TodosException(Exception):
    """
    Base class for TODOs specific exceptions.
    """

    def __init__(self, value):
        """
        Class constructor.
        """
        super(TodosException, self).__init__()

        self.value = value
        # """ The exception value. """

    def __str__(self):
        """
        Return a string representation of the exception.
        """
        return repr(self.value)


###############################################################################
####

class TodosFatalError(TodosException):
    """
    Fatal error in TODOs.
    """
    pass
