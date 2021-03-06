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
Simple logger.
"""


###############################################################################
####

import sys


###############################################################################
####

class Logger(object):
    """
    A simple logger class.
    """


    def __init__(self, verbose_enabled):
        """
        Class constructor.
        """
        self.verbose_enabled = verbose_enabled
        # """ Flag to enable the verbose mode. """


    def verbose(self, message):
        """
        Output a verbose message to the standard output stream if verbose mode
        is enabled.
        """
        if self.verbose_enabled:
            sys.stdout.write(message)
            sys.stdout.write('\n')


    def warn(self, message):
        """
        Output a warning message to the standard error stream.
        """
        sys.stderr.write('WARN: {0}'.format(message))
        sys.stderr.write('\n')


    def error(self, message):
        """
        Output an error message to the standard error stream.
        """
        sys.stderr.write('ERROR: {0}'.format(message))
        sys.stderr.write('\n')
