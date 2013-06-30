#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Michal Turek
#
# This file is part of todos.
# http://todos.sourceforge.net/
#
# todos is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# todos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with todos.  If not, see <http://www.gnu.org/licenses/>.
#


"""
Output the data in TXT format.
"""


###############################################################################
####

class TxtFormatter:
    """
    Text formatter.
    """

    MULTILINE_DELIMITER = '--'
    # """ Delimiter if multiline output is enabled. """


    def __init__(self, multiline):
        """
        Class constructor.
        """
        self.multiline = multiline
        # """ Multiple lines per pattern will be passed to the output. """


    def get_type(self):
        """
        Return type of the formatter.
        """
        return 'TXT'


    def write_header(self, out_stream):
        """
        Write the header to the output stream.
        """
        # Empty
        pass


    def write_data(self, out_stream, comments, summary):
        """
        Write the data to the output stream.
        """
        if self.multiline:
            print >> out_stream, self.MULTILINE_DELIMITER

        for comment in comments:
            position = comment.position

            for line in comment.lines:
                print >> out_stream, '{0}:{1}: {2}'.format(
                        comment.path, position, line)
                position += 1

            if self.multiline:
                print >> out_stream, self.MULTILINE_DELIMITER


    def write_footer(self, out_stream):
        """
        Write the footer to the output stream.
        """
        # Empty
        pass
