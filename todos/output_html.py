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
Output the data in HTML format.
"""


###############################################################################
####

import sys
import os
import socket
from operator import itemgetter
from time import localtime, strftime

import version


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
/* backgroud-color: white; */
#sidebar    { position: fixed; top: 0px; left: 0px; width: 14%; padding: 2em;
                background-color: white; }
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
        print >> out_stream, '<p id="footer">'
        print >> out_stream, 'Page generated: {0}, {1} {2}'.format(
                strftime("%Y-%m-%d %H:%M:%S", localtime()),
                self.html_link('http://todos.sourceforge.net/', 'todos'),
                version.TodosVersion.VERSION)
        print >> out_stream, '</p>'
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
