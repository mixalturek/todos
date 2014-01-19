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
The application logic.
"""


###############################################################################
####

import argparse
import sys
import codecs

from . import logger
from . import search
from . import output
from . import version


###############################################################################
#### Configuration, default values



COMMENTS = ['#', '//', '/*', '<!--']
PATTERNS = [r'\bTODO\b', r'\bFIXME\b']
SUPPRESSED = ['.git', '.svn', 'CVS']
DIRECTORIES = ['.']
NUM_LINES = 1
ENCODING = 'utf-8'


###############################################################################
####

class Todos(object):
    """
    Top level module class that contains enter to the application. It drives
    parsing of the input files, searching comments and output of the results.
    """


    def __init__(self):
        """
        Class constructor.
        """

        self.logger = logger.Logger(False) # Will be redefined in main()
        # """ The logger used in the application. """


    def main(self, argv):
        """
        Enter the application.
        """
        parameters = self.parse_command_line_arguments(argv)
        self.logger = logger.Logger(parameters.verbose)
        self.dump_parameters(parameters)

        comments_search = search.CommentsSearch(parameters, self.logger)
        comments_search.search()

        output_writer = output.OutputWriter(parameters, self.logger)
        output_writer.output(comments_search)


    def parse_command_line_arguments(self, argv):
        """
        Parse all command line arguments and return them in object form.
        """
        parser = argparse.ArgumentParser(
                prog='todos.sh',
                description='Search project directory for TODO, FIXME '
                        'and similar comments.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        parser.add_argument(
                '-V', '--version',
                help='show version and exit',
                action='version',
                version='%(prog)s ' + version.TodosVersion.VERSION
        )

        parser.add_argument(
                '-v', '--verbose',
                help='increase output verbosity',
                action='store_true',
                default=False
        )

        parser.add_argument(
                '-c', '--comment',
                nargs='+',
                help='the comment characters',
                metavar='COMMENT',
                dest='comments',
                default=COMMENTS
        )

        parser.add_argument(
                '-e', '--regexp',
                nargs='+',
                help='pattern to search; see Python re module for '
                        'proper syntax',
                metavar='PATTERN',
                dest='patterns',
                default=PATTERNS
        )

        parser.add_argument(
                '-A', '--after-context',
                type=int,
                metavar='NUM',
                dest='num_lines',
                help='number of lines that are sent to the output together '
                        'with the matching line',
                default=NUM_LINES
        )

        parser.add_argument(
                '-t', '--file-ext',
                metavar='EXT',
                nargs='+',
                help='check only files with the specified extension',
                dest='extensions'
        )

        parser.add_argument(
                '-D', '--suppressed',
                metavar='DIR',
                nargs='+',
                help='suppress the specified directory; directory name or path',
                default=SUPPRESSED
        )

        parser.add_argument(
                '-n', '--encoding',
                help='the files encoding',
                default=ENCODING
        )

        parser.add_argument(
                '-i', '--ignore-case',
                action='store_true',
                help='ignore case distinctions',
                dest='ignore_case',
                default=False
        )

        parser.add_argument(
                '-o', '--out-txt',
                metavar='TXT',
                dest='out_txt',
                help='output text file; standard output will be used if '
                        'no output file is specified'
        )

        parser.add_argument(
                '-x', '--out-xml',
                metavar='XML',
                dest='out_xml',
                help='output XML file'
        )

        parser.add_argument(
                '-m', '--out-html',
                metavar='HTML',
                dest='out_html',
                help='output HTML file'
        )

        parser.add_argument(
                '-f', '--force',
                action='store_true',
                default=False,
                help='override existing output files'
        )

        parser.add_argument(
                'directory',
                nargs='*',
                help='the input directory to search in',
                metavar='DIRECTORY',
                # ValueError: dest supplied twice for positional argument
                # dest='directories',
                default=DIRECTORIES
        )

        parameters = parser.parse_args(argv)

        # Workaround for ValueError: dest supplied twice for positional argument
        parameters.directories = parameters.directory

        self.verify_parameters(parameters)

        return parameters


    def dump_parameters(self, parameters):
        """
        Dump values of parameters if a verbose output is enabled.
        """
        self.logger.verbose('Command line arguments:')
        self.logger.verbose(' '.join(sys.argv))
        self.logger.verbose('')

        self.logger.verbose('Parsed command line arguments:')
        self.logger.verbose('verbose: {0}'.format(parameters.verbose))
        self.logger.verbose('comments: {0}'.format(parameters.comments))
        self.logger.verbose('patterns: {0}'.format(parameters.patterns))
        self.logger.verbose('extensions: {0}'.format(parameters.extensions))
        self.logger.verbose('suppressed-dirs: {0}'.format(
        parameters.suppressed))
        self.logger.verbose('encoding: {0}'.format(parameters.encoding))
        self.logger.verbose('ignore-case: {0}'.format(parameters.ignore_case))
        self.logger.verbose('num-lines: {0}'.format(parameters.num_lines))
        self.logger.verbose('out-txt: {0}'.format(parameters.out_txt))
        self.logger.verbose('out-xml: {0}'.format(parameters.out_xml))
        self.logger.verbose('out-html: {0}'.format(parameters.out_html))
        self.logger.verbose('force: {0}'.format(parameters.force))
        self.logger.verbose('directories: {0}'.format(parameters.directories))
        self.logger.verbose('')


    def verify_parameters(self, parameters):
        """
        Verify values of the input parameters.
        """
        try:
            codecs.lookup(parameters.encoding)
        except LookupError as lookup_exception:
            self.logger.warn('Encoding error: {0}'.format(lookup_exception))
            self.logger.warn('Changing encoding to default: {0}'.
                    format(ENCODING))
            parameters.encoding = ENCODING

        if parameters.extensions is not None:
            tmp_extensions = []

            for extension in parameters.extensions:
                if extension.startswith('.'):
                    tmp_extensions.append(extension)
                else:
                    tmp_extensions.append('.' + extension)

            parameters.extensions = tmp_extensions
