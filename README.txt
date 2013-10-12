NAME
====

TODOs - search TODO, FIXME and similar comments in project files

SYNOPSIS
========

todos [OPTIONS] DIRECTORY [DIRECTORY...]

DESCRIPTION
===========

TODOs is a small command-line utility to search TODO, FIXME and similar
comments in project files. It is licensed under the terms of GNU GPL 3
license, it requires Python 3 interpreter for its execution and it is
not platform specific.

OPTIONS
=======

positional arguments:
---------------------

    DIRECTORY             the input directory to search in (default:
                          ['.'])

optional arguments:
-------------------

    -h, --help            show this help message and exit
    -V, --version         show version and exit
    -v, --verbose         increase output verbosity (default: False)
    -c COMMENT [COMMENT ...], --comment COMMENT [COMMENT ...]
                          the comment characters (default: ['#',
                          '//', '/*'])
    -e PATTERN [PATTERN ...], --regexp PATTERN [PATTERN ...]
                          the pattern to search; see Python re module
                          for proper syntax (default: ['\\bTODO\\b',
                          '\\bFIXME\\b'])
    -A NUM, --after-context NUM
                          number of lines that are sent to the output
                          together with the matching line (default:
                          1)
    -t EXT [EXT ...], --file-ext EXT [EXT ...]
                          check only files with the specified
                          extension (default: None)
    -D DIR [DIR ...], --suppressed DIR [DIR ...]
                          suppress the specified directory (default:
                          ['.git', '.svn', 'CVS'])
    -n ENCODING, --encoding ENCODING
                          the files encoding (default: utf-8)
    -i, --ignore-case     ignore case distinctions (default: False)
    -o TXT, --out-txt TXT
                          the output text file; standard output will
                          be used if the path is not specified
                          (default: None)
    -x XML, --out-xml XML
                          the output XML file (default: None)
    -m HTML, --out-html HTML
                          the output HTML file (default: None)
    -f, --force           override existing output files (default:
                          False)

SEE ALSO
========

See the TODOs website at http://todos.sourceforge.net/.

AUTHOR
======

Written by Michal Turek.

COPYRIGHT
=========

Copyright (C) 2013 Michal Turek. This file is part of TODOs.

TODOs is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation, version 3 of the License.

TODOs is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along
with TODOs. If not, see http://www.gnu.org/licenses/.
