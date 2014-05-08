# NAME
TODOs - search TODO, FIXME and similar comments in project files


# SYNOPSIS
    todos.sh [OPTIONS] DIRECTORY [DIRECTORY...]


# DESCRIPTION
**TODOs** is a small command-line utility to search TODO, FIXME and similar
comments in project files. It is written in Python 3 and licensed under the
terms of GNU GPL 3 license. Supported output formats are TXT, HTML and XML.

## Features

- Recursive scan of specific file types in a directory and its subdirectories.
- Directories as CVS, .svn and .git can be suppressed.
- Scanned files can be limited only to specific file types as .java, .py or .cpp.
- Search patterns are defined as Python's regular expressions.
- A line with the occurrence can be output together with a close context around.
- TXT, HTML and XML output formats.
- Suitable for continuous integration.


# OPTIONS
## positional arguments:
    DIRECTORY             the input directory to search in (default:
                          ['.'])

## optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show version and exit
    -v, --verbose         increase output verbosity (default: False)
    -c COMMENT [COMMENT ...], --comment COMMENT [COMMENT ...]
                          the comment characters (default: ['#',
                          '//', '/*', '<!--'])
    -e PATTERN [PATTERN ...], --regexp PATTERN [PATTERN ...]
                          pattern to search; see Python re module for
                          proper syntax (default: ['\\bTODO\\b',
                          '\\bFIXME\\b'])
    -A NUM, --after-context NUM
                          number of lines that are sent to the output
                          together with the matching line (default:
                          1)
    -t EXT [EXT ...], --file-ext EXT [EXT ...]
                          check only files with the specified
                          extension (default: None)
    -D DIR [DIR ...], --suppressed DIR [DIR ...]
                          suppress the specified directory; directory
                          name or path (default: ['.git', '.svn',
                          'CVS'])
    -n ENCODING, --encoding ENCODING
                          the files encoding (default: utf-8)
    -i, --ignore-case     ignore case distinctions (default: False)
    -o TXT, --out-txt TXT
                          output text file; standard output will be
                          used if no output file is specified
                          (default: None)
    -x XML, --out-xml XML
                          output XML file (default: None)
    -m HTML, --out-html HTML
                          output HTML file (default: None)
    -f, --force           override existing output files (default:
                          False)

# EXAMPLES

Show help and exit.

    todos.sh -h


Search default comments with default settings in a current directory and display the results on standard output.

    todos.sh


Search default comments with verbose/debug output, rewrite any output file if it exists, skip .git and build directories and put the results to three files in TXT, XML and HTML formats.

    todos.sh -v -f -D .git build -o todos.txt -x todos.xml -m todos.html


Search TODO, FIXME, OPEN and @2-3 letters@ in all files under src directory, ignore case, append additional lines that follows the line with the occurrence and generate a HTML report.

    todos.sh -f -e '\\bTODO\\b' '\\bFIXME\\b' '\\bOPEN\\b' '@[a-zA-Z]{2,3}@' \
             -i -A 5 -m todos.html src


# BUGS

No bugs are known at the moment.


# SEE ALSO
See the TODOs website at [http://todos.sourceforge.net/](http://todos.sourceforge.net/).


# AUTHOR
Written by Michal Turek.


# COPYRIGHT
Copyright (C) 2013 Michal Turek.  This file is part of TODOs.

TODOs is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

TODOs is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with TODOs.  If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
