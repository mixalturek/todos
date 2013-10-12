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
Output the data.
"""


###############################################################################
####

import sys
import os.path
import codecs

from . import output_txt
from . import output_xml
from . import output_html


###############################################################################
####

class OutputWriter:
    """
    Write the results of the searching to the output files in specified formats.
    """


    def __init__(self, parameters, logger):
        """
        Class constructor.
        """
        self.parameters = parameters
        # """ The input parameters. """

        self.logger = logger
        # """ The logger to output messages. """


    def output(self, comments_search):
        """
        Determine which formats are requested and store them to the appropriate
        files. If no output file is specified, use the standard output stream.
        """
        output_written = False

        self.logger.verbose('') # New line to split the output

        if self.parameters.out_txt is not None:
            self.output_data_to_file(self.parameters.out_txt,
                    output_txt.TxtFormatter(self.parameters.num_lines > 1),
                    comments_search)
            output_written = True

        if self.parameters.out_xml is not None:
            self.output_data_to_file(self.parameters.out_xml,
                    output_xml.XmlFormatter(self.parameters), comments_search)
            output_written = True

        if self.parameters.out_html is not None:
            self.output_data_to_file(self.parameters.out_html,
                    output_html.HtmlFormatter(self.parameters), comments_search)
            output_written = True

        # Use stdout if no output method is explicitly specified
        if output_written == False:
            self.output_data(sys.stdout,
                    output_txt.TxtFormatter(self.parameters.num_lines > 1),
                    comments_search)


    def output_data_to_file(self, path, formatter, comments_search):
        """
        Open the output file and write the data.
        """
        self.logger.verbose('Writing {0} output: {1}'.
                format(formatter.get_type(), path))

        if os.path.exists(path) and not self.parameters.force:
            self.logger.warn('File exists, use force parameter to '
                    'override: {0}'.format(path))
            return

        try:
            with codecs.open(path, 'w', self.parameters.encoding) as out_stream:
                self.output_data(out_stream, formatter, comments_search)
        except IOError as io_exception:
            self.logger.error('Output failed: {0}, {1}'.format(
                    path, io_exception))
            return


    def output_data(self, out_stream, formatter, comments_search):
        """
        Output the data to the opened stream and use the specified formatter.
        """
        formatter.write_header(out_stream)
        formatter.write_data(out_stream, comments_search.comments,
                comments_search.summary)
        formatter.write_footer(out_stream)
