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
Search TODO, FIXME and similar comments in project files.
"""


import argparse
import os
import os.path
import sys
import re
import socket
import codecs
from time import localtime, strftime
from operator import itemgetter


###############################################################################
#### Configuration, default values

TODOS_VERSION = '0.1.0'
XML_VERSION = '0.1.0'

COMMENTS = ['#', '//', '/*']
PATTERNS = [r'\bTODO\b', r'\bFIXME\b']
SUPPRESSED = ['.git', '.svn', 'CVS']
DIRECTORIES = ['.']
NUM_LINES = 1
ENCODING = 'utf-8'


###############################################################################
####

class Todos:
    """
    Top level module class that contains enter to the application. It drives
    parsing of the input files, searching comments and output of the results.
    """


    def __init__(self):
        """
        Class constructor.
        """

        self.logger = Logger(False) # Will be redefined in main()
        # """ The logger used in the application. """


    def main(self, argv):
        """
        Enter the application.
        """
        parameters = self.parse_command_line_arguments(argv)
        self.logger = Logger(parameters.verbose)
        self.dump_parameters(parameters)

        comments_search = CommentsSearch(parameters, self.logger)
        comments_search.search()

        output_writer = OutputWriter(parameters, self.logger)
        output_writer.output(comments_search)


    def parse_command_line_arguments(self, argv):
        """
        Parse all command line arguments and return them in object form.
        """
        parser = argparse.ArgumentParser(
                prog='todos',
                description='Search project directory for TODO, FIXME '
                        'and similar comments.',
                formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        parser.add_argument(
                '-V', '--version',
                help='show version and exit',
                action='version',
                version='%(prog)s ' + TODOS_VERSION
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
                help='the pattern to search; see Python re module for '
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
                help='suppress the specified directory',
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
                help='the output text file; standard output will be used if '
                        'the path is not specified'
        )

        parser.add_argument(
                '-x', '--out-xml',
                metavar='XML',
                dest='out_xml',
                help='the output XML file'
        )

        parser.add_argument(
                '-m', '--out-html',
                metavar='HTML',
                dest='out_html',
                help='the output HTML file'
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


###############################################################################
####

class Logger:
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
            print message


    def warn(self, message):
        """
        Output a warning message to the standard error stream.
        """
        print >> sys.stderr, 'WARN:', message


    def error(self, message):
        """
        Output an error message to the standard error stream.
        """
        print >> sys.stderr, 'ERROR:', message


###############################################################################
####

class Comment:
    """
    Container to store one comment that was found.
    """

    def __init__(self, str_pattern, path, position, lines):
        """
        Class constructor, initialize all members.
        """
        self.str_pattern = str_pattern
        # """ The pattern that was searched and found. """

        self.path = path
        # """ The input file. """

        self.position = position
        # """ The position in the file. """

        self.lines = lines
        # """ The matching line and optionally several lines after it. """


###############################################################################
####

class Pattern:
    """
    Container to store one pattern (regular expression) for searching.
    """


    def __init__(self, str_pattern, re_pattern):
        """
        Class constructor, initialize all members.
        """
        self.str_pattern = str_pattern
        # """ The string representation of the pattern. """

        self.re_pattern = re_pattern
        # """ The precompiled pattern. """


    def __str__(self):
        """
        Return a string representation of the pattern.
        """
        return self.str_pattern


###############################################################################
####

class Summary:
    """
    Container to store a summary of the comments searching.
    """

    def __init__(self, parameters):
        """
        Class constructor, initialize all members to zero or empty list.
        """
        self.total_files = 0
        # """ The number of the examined files. """

        self.total_directories = 0
        # """ The number of the examined directories. """

        self.per_pattern = {}
        # """ Summary per pattern. """

        self.per_file = {}
        # """ Summary per file. """

        for str_pattern in parameters.patterns:
            self.per_pattern[str_pattern] = 0


###############################################################################
####

class CommentsSearch:
    """
    Search comments in the source files.
    """

    def __init__(self, parameters, logger):
        """
        Class constructor, prepare the object for searching.
        """
        self.parameters = parameters
        # """ The input parameters. """

        self.logger = logger
        # """ The logger to output messages. """

        self.comments = []
        # """ The comments that was found during the searching. """

        self.summary = Summary(parameters)
        # """ The summary of the searching. """

        flags = 0
        if self.parameters.ignore_case:
            flags = re.IGNORECASE

        self.parameters.compiled_patterns = []
        for str_pattern in self.parameters.patterns:
            try:
                self.parameters.compiled_patterns.append(
                        Pattern(str_pattern, re.compile(str_pattern, flags))
                )
            except re.error as re_exception:
                self.logger.warn('Pattern compilation failed: {0}, {1}'.
                        format(str_pattern, re_exception))


    def search(self):
        """
        Recursively search the comments according to the input parameters.
        """
        self.process_directories()


    def process_directories(self):
        """
        Process all directories.
        """
        for directory in self.parameters.directories:
            self.process_directory(directory, directory)


    def is_directory_suppressed(self, dir_name):
        """
        Return true if the input directory should be skipped, otherwise false.
        """
        if self.parameters.suppressed is None:
            return False

        return dir_name in self.parameters.suppressed


    def process_directory(self, directory, dir_name):
        '''
        Recursively search files in the input directory.
        '''
        if not os.path.isdir(directory):
            self.logger.verbose('Skipping directory (not a directory): {0}'.
                    format(directory))
            return

        if self.is_directory_suppressed(dir_name):
            self.logger.verbose('Skipping directory (suppressed): {0}'.
                    format(directory))
            return

        self.summary.total_directories += 1

        for item in os.listdir(directory):
            path = os.path.join(directory, item)

            if os.path.isfile(path):
                self.process_file(path)
            else:
                self.process_directory(path, item)


    def is_file_extension_allowed(self, path):
        """
        Return true if the input file should be processed, otherwise false.
        """
        if self.parameters.extensions is None:
            return True

        for extension in self.parameters.extensions:
            if path.endswith(extension):
                return True

        return False


    def is_file_binary(self, path):
        """
        Return true if the input file is considered as binary, otherwise false.
        Note the return value may be incorrect, only beginning of the file is
        examined for '\0' character.
        """
        const_chunk_size = 1024

        try:
            with open(path, 'rb') as input_file:
                chunk = input_file.read(const_chunk_size)
        except IOError as io_exception:
            self.logger.warn('Reading from file failed: {0}, {1}'.
                    format(path, io_exception))
            return True

        # If the beginning of the file contains a null byte, guess that the
        # file is binary. GNU grep works similarly, see file_is_binary()
        # in its source codes.
        #
        # The following works nicely for common ascii/utf8 encoded source codes
        # with binary object files, images and jar packages in the same
        # directory tree. The heuristic can be extended in future if needed,
        #
        # Note UTF-16 encoded text files will be clasified as binary,
        # is it correct/incorrect?
        return '\0' in chunk


    def process_file(self, path):
        '''
        Process all lines of the input file.
        '''
        if not self.is_file_extension_allowed(path):
            self.logger.verbose('Skipping file (file extension): {0}'.
                    format(path))
            return

        if self.is_file_binary(path):
            self.logger.verbose('Skipping file (binary file): {0}'.format(path))
            return

        self.logger.verbose('Parsing file: {0}'.format(path))

        try:
            with codecs.open(path, 'r', self.parameters.encoding) as input_file:
                lines = input_file.readlines()

            self.summary.total_files += 1
            self.summary.per_file[path] = 0

            position = 0
            for line in lines:
                position += 1
                self.process_line(path, position, line, lines)
        except IOError as io_exception:
            self.logger.warn('Reading from file failed: {0}, {1}'.
                    format(path, io_exception))
        except UnicodeError:
            self.logger.warn('Skipping file (unicode error): {0}'.format(path))


    def contains_comment(self, line):
        """
        Return true if the input line contains a comment, otherwise false.
        """
        for comment in self.parameters.comments:
            if line.count(comment) > 0:
                return True

        return False


    def process_line(self, path, position, line, lines):
        '''
        Process the input line, search comment with one of the specified
        patterns.
        '''
        if not self.contains_comment(line):
            return

        for pattern in self.parameters.compiled_patterns:
            if pattern.re_pattern.search(line):
                lines_to_store = self.get_lines(lines, position-1,
                        self.parameters.num_lines)
                self.comments.append(Comment(pattern.str_pattern, path,
                        position, lines_to_store))
                self.summary.per_pattern[pattern.str_pattern] += 1
                self.summary.per_file[path] += 1
                break


    def get_lines(self, lines, position, count):
        '''
        Return content of the specified number of lines.
        '''
        last_line = position+count
        if last_line >= len(lines):
            last_line = len(lines)

        result = []
        for i in range(position, last_line):
            result.append(lines[i].rstrip())

        return result


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
                    TxtFormatter(self.parameters.num_lines > 1),
                    comments_search)
            output_written = True

        if self.parameters.out_xml is not None:
            self.output_data_to_file(self.parameters.out_xml,
                    XmlFormatter(self.parameters), comments_search)
            output_written = True

        if self.parameters.out_html is not None:
            self.output_data_to_file(self.parameters.out_html,
                    HtmlFormatter(self.parameters), comments_search)
            output_written = True

        # Use stdout if no output method is explicitly specified
        if output_written == False:
            self.output_data(sys.stdout,
                    TxtFormatter(self.parameters.num_lines > 1),
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


###############################################################################
####

# TODO: summary in XML

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
                TODOS_VERSION, XML_VERSION)
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


###############################################################################
####

class HtmlFormatter:
    """
    HTML formatter.
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
        return 'HTML'


    def write_header(self, out_stream):
        """
        Write the header to the output stream.
        """
        print >> out_stream, '''<?xml version="1.0" encoding="{0}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
        "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
<meta http-equiv="content-type" content="text/html; charset={0}" />
<meta http-equiv="content-language" content="en" />
<title>Comments Report - todos</title>
'''.format(self.parameters.encoding)

        print >> out_stream, '''
<style type="text/css" media="all">
body
{
    margin: 2em; padding: 0px;
    background-color: white; color: black;
    font-family: Verdana, "Bitstream Vera Sans", Geneva, Arial, sans-serif;
    font-size: 10pt; line-height: 1.6em;
}

pre         { line-height: 1.1em; margin: 0; margin: 0.2em 0 0.2em 0; }
a:hover     { color: blue; }

table       { margin-top: 1em; margin-bottom: 1em; max-width: 100%; }
th          { background-color: #AFB3CC; text-align: left; }
th, td      { vertical-align: top; padding: 0.2em 0.5em 0.2em 0.5em; }
tr          { background-color: #D0D0EE; }
tr:hover    { background-color: #C0C0FF; }

#page       { margin-left: 17%; }
#sidebar    { position: fixed; top: 0px; left: 0px; width: 15%; padding: 2em; }
#footer     { font-size: 9pt; margin-top: 2em; border-top: 1px solid silver;
              color: gray; clear: both; }

#sidebar .menu_title { font-weight: bold; font-size: 14pt; }
#sidebar ul { margin-left: 1em; padding-left: 0px; }
#sidebar ul ul { margin-left: 2em; padding-left: 0px; }
</style>

<style type="text/css" media="print">
#page       { margin-left: 0px; }
#sidebar    { display: none; }
</style>

</head>

<body>
'''


    def write_data(self, out_stream, comments, summary):
        """
        Write the data to the output stream.
        """
        print >> out_stream, '<div id="sidebar">'

        self.write_toc(out_stream)

        print >> out_stream, '</div><!-- id="sidebar" -->'


        print >> out_stream, '<div id="page">'

        print >> out_stream, '<h1 id="commentsReport">Comments Report</h1>'

        print >> out_stream, '<h2 id="inputParameters">Input Parameters</h2>\n'
        self.write_input_parameters(out_stream)

        print >> out_stream, '<h2 id="summary">Summary</h2>\n'

        print >> out_stream, '<h3 id="general">General</h3>\n'
        self.write_general_summary(out_stream, summary)

        print >> out_stream, '<h3 id="per_patterns">Per Patterns</h3>\n'
        self.write_per_pattern(out_stream, summary.per_pattern)

        print >> out_stream, '<h3 id="per_files">Per Files</h3>\n'
        self.write_per_file(out_stream, summary.per_file)

        print >> out_stream, '<h2 id="details">Details</h2>\n'
        self.write_comments(out_stream, comments)

        print >> out_stream, '</div><!-- id="page" -->'


    def write_toc(self, out_stream):
        """
        Write table of contents as menu.
        """
        print >> out_stream, '''
<div class="menu_title">Menu</div>

<ul>
<li><a href="#commentsReport">Comments Report</a>
    <ul>
    <li><a href="#inputParameters">Input Parameters</a></li>
    <li><a href="#summary">Summary</a>
        <ul>
        <li><a href="#general">General</a></li>
        <li><a href="#per_patterns">Per Patterns</a></li>
        <li><a href="#per_files">Per Files</a></li>
        </ul>
    </li>
    <li><a href="#details">Details</a></li>
    </ul>
</li>
</ul>
'''


    def write_input_parameters(self, out_stream):
        """
        Write input parameters as a table.
        """
        rows = [['Computer', self.html_special_chars(socket.gethostname())],
                ['User', self.html_special_chars(os.environ['LOGNAME'])],
                ['Python', self.html_special_chars('.'.join(
                        [str(v) for v in sys.version_info[0:3]]))],
        ]
        self.html_table(out_stream, ['Parameter', 'Value'], rows)

        print >> out_stream, '<pre>'
        print >> out_stream, 'cd {0}'.format(
                self.html_special_chars(os.getcwd()))
        print >> out_stream, self.html_special_chars(' '.join(sys.argv))
        print >> out_stream, '</pre>\n'

        rows = [['Working Directory', self.html_special_chars(
                        os.getcwd())],
                ['Verbose', self.html_special_chars(
                        str(self.parameters.verbose))],
                ['Comments', self.html_special_chars(
                        str(self.parameters.comments))],
                ['Patterns', self.html_special_chars(
                        str(self.parameters.patterns))],
                ['Extensions', self.html_special_chars(
                        str(self.parameters.extensions))],
                ['Suppressed Directories', self.html_special_chars(
                        str(self.parameters.suppressed))],
                ['Encoding', self.html_special_chars(
                        str(self.parameters.encoding))],
                ['Ignore Case', self.html_special_chars(
                        str(self.parameters.ignore_case))],
                ['Number of Lines', self.html_special_chars(
                        str(self.parameters.num_lines))],
                ['Output TXT File', self.html_special_chars(
                        str(self.parameters.out_txt))],
                ['Output XML File', self.html_special_chars(
                        str(self.parameters.out_xml))],
                ['Output HTML File', self.html_special_chars(
                        str(self.parameters.out_html))],
                ['Force', self.html_special_chars(
                        str(self.parameters.force))],
                ['Directories', self.html_special_chars(
                        str(self.parameters.directories))],
        ]
        self.html_table(out_stream, ['Parameter', 'Value'], rows)


    def write_general_summary(self, out_stream, summary):
        """
        Write summary as a table.
        """
        num_files_with_matches = 0
        for path, count in summary.per_file.iteritems():
            if count != 0:
                num_files_with_matches += 1

        rows = [['Searched Patterns', len(summary.per_pattern)],
                ['Files with Matches', num_files_with_matches],
                ['Total Files', summary.total_files],
                ['Total Directories', summary.total_directories]
        ]
        self.html_table(out_stream, ['Parameter', 'Value'], rows)


    def write_per_pattern(self, out_stream, per_pattern):
        """
        Write table of the input patterns together with the number of their
        occurrences.
        """
        rows = [[self.html_special_chars(str_pattern), comment]
                for str_pattern, comment in per_pattern.iteritems()]
        rows.sort(key=itemgetter(1), reverse=True)
        self.html_table(out_stream, ['Pattern', 'Occurrences'], rows)


    def write_per_file(self, out_stream, per_file):
        """
        Write table of the input files together with the number of the
        occurrences. Skip files with no occurrences.
        """
        rows = []

        for path, count in per_file.iteritems():
            if count > 0:
                rows.append([self.html_link(os.path.abspath(path), path),
                        count])

        rows.sort(key=itemgetter(1), reverse=True)
        self.html_table(out_stream, ['File', 'Occurrences'], rows)


    def write_comments(self, out_stream, comments):
        """
        Write table of all occurrences with all details.
        """
        rows = []

        for comment in comments:
            path = self.html_link(os.path.abspath(comment.path), comment.path)
            str_pattern = self.html_special_chars(comment.str_pattern)
            content = '<pre>{0}</pre>'.format(self.html_special_chars(
                    '\n'.join(comment.lines)))
            rows.append([path, comment.position, str_pattern, content])

        self.html_table(out_stream, ['File', 'Line', 'Pattern', 'Content'],
                rows)


    def write_footer(self, out_stream):
        """
        Write the footer to the output stream.
        """
        print >> out_stream, '<p id="footer">Page generated: {0}, {1}, {2}.'
        '</p>'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()),
                self.html_link('http://todos.sourceforge.net/', 'todos'),
                TODOS_VERSION)
        print >> out_stream, '</body>'
        print >> out_stream, '</html>'


    def html_special_chars(self, text):
        """
        Replace all special characters by the HTML entities and return a new
        string.
        """
        ret = text
        ret = ret.replace('&', '&amp;')
        ret = ret.replace('"', '&quot;')
        ret = ret.replace('<', '&lt;')
        ret = ret.replace('>', '&gt;')
        return ret


    def html_link(self, target, text):
        """
        Return a HTML link constructed from a target address and a label.
        """
        return '<a href="{0}">{1}</a>'.format(
                self.html_special_chars(target),
                self.html_special_chars(text)
        )


    def html_table(self, out_stream, headers, rows):
        """
        Write a HTML table to the output stream.
        """
        print >> out_stream, '<table>\n<thead>\n<tr>'

        for header in headers:
            print >> out_stream, '<th>{0}</th>'.format(header)

        print >> out_stream, '</tr>\n</thead>\n\n<tbody>\n'

        for row in rows:
            print >> out_stream, '<tr>'

            for item in row:
                print >> out_stream, '<td>{0}</td>'.format(item)

            print >> out_stream, '</tr>\n'


        print >> out_stream, '</tbody>\n</table>\n'


###############################################################################
####

if __name__ == '__main__':
    try:
        TODOS = Todos()
        TODOS.main(sys.argv[1:])
    except KeyboardInterrupt as keyboard_exception:
        sys.exit('\nERROR: Interrupted by user')
