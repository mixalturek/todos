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
Version informations.
"""


###############################################################################
####

class TodosVersion:
    """
    Version informations.
    """

    def __init__(self):
        """
        Class constructor.
        """
        pass


    VERSION_MAJOR = 0
    # """ Major version of the application. """

    VERSION_MINOR = 1
    # """ Minor version of the application. """

    VERSION_REVISION = 0
    # """ Revision of the application. """

    VERSION = '{0}.{1}.{2}'.format(VERSION_MAJOR, VERSION_MINOR,
            VERSION_REVISION)
    # """ Concatenated version parts of the application. """


    XML_VERSION_MAJOR = 0
    # """ Major version of the XML output format. """

    XML_VERSION_MINOR = 1
    # """ Minor version of the XML output format. """

    XML_VERSION_REVISION = 0
    # """ Revision of the XML output format. """

    XML_VERSION = '{0}.{1}.{2}'.format(XML_VERSION_MAJOR, XML_VERSION_MINOR,
            XML_VERSION_REVISION)
    # """ Concatenated version parts of the XML output format. """
