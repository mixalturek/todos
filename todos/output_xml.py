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
Output the data in XML format.
"""


###############################################################################
####

import xml.etree.ElementTree as etree

from . import version


###############################################################################
####

class XmlFormatter(object):
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
        pass


    def write_data(self, out_stream, comments, summary):
        """
        Write the data to the output stream.
        """
        el_comments = etree.Element('{http://todos.sourceforge.net}comments',
                attrib = {
                    '{http://todos.sourceforge.net}version':
                            version.TodosVersion.VERSION,
                })

        for comment in comments:
            el_comment = etree.SubElement(
                el_comments, '{http://todos.sourceforge.net}comment',
                attrib = {
                    '{http://todos.sourceforge.net}pattern':comment.str_pattern,
                    '{http://todos.sourceforge.net}file':comment.path,
                    '{http://todos.sourceforge.net}line':str(comment.position)
                }
            )

            el_comment.text = '\n'.join(comment.lines)

        self.indent(el_comments)
        tree = etree.ElementTree(el_comments)

        tree.write(out_stream,
            encoding="unicode",
            xml_declaration=True,
            default_namespace='http://todos.sourceforge.net',
            method="xml")


    def write_footer(self, out_stream):
        """
        Write the footer to the output stream.
        """
        pass


    def indent(self, elem, level=0):
        """
        Pretty print the XML document.
        http://effbot.org/zone/element-lib.htm#prettyprint
        """
        i = '\n' + level*'\t'
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + '\t'
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self.indent(elem, level+1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
