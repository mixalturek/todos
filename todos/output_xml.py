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
Output the data in XML format.
"""


###############################################################################
####

import version


###############################################################################
####

class XmlFormatter:
    """
    XML formatter.
    """


    def __init__(self, parameters):
        """
        Class constructor.
        """
        self.parameters = parameters
        # """ The input parameters. """


    def get_type(self):
        """
        Return type of the formatter.
        """
        return 'XML'


    def write_header(self, out_stream):
        """
        Write the header to the output stream.
        """
        print >> out_stream, '<?xml version="1.0" encoding="{0}" '
        'standalone="yes"?>'.format(self.parameters.encoding)

        print >> out_stream, '<Todos>'
        print >> out_stream, '\t<Version todos="{0}" format="{1}">'.format(
                version.TodosVersion.VERSION, version.TodosVersion.XML_VERSION)
        print >> out_stream, '\t<Comments>'


    def write_data(self, out_stream, comments, summary):
        """
        Write the data to the output stream.
        """
        for comment in comments:
            print >> out_stream, '\t\t<Comment pattern="{0}" file="{1}" '
            'line="{2}">'.format(
                    self.xml_special_chars(comment.str_pattern),
                    self.xml_special_chars(comment.path),
                    comment.position)

            for line in comment.lines:
                print >> out_stream, '\t\t\t{0}'.format(
                        self.xml_special_chars(line))

            print >> out_stream, '\t\t</Comment>'


    def write_footer(self, out_stream):
        """
        Write the footer to the output stream.
        """
        print >> out_stream, '\t</Comments>'
        print >> out_stream, '</Todos>'


    def xml_special_chars(self, text):
        """
        Replace all special characters by the XML entities and
        return a new string.
        """
        ret = text
        ret = ret.replace('&', '&amp;')
        ret = ret.replace('"', '&quot;')
        ret = ret.replace('<', '&lt;')
        ret = ret.replace('>', '&gt;')
        return ret
