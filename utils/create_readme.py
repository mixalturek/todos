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


import sys
import re

README_FILE = 'README.md'
help_text = sys.stdin.read()

with open('utils/' + README_FILE + '.in') as input_file:
    old_readme = input_file.read()

header = old_readme[:old_readme.index('# OPTIONS')]
footer = old_readme[old_readme.index('# SEE ALSO'):]

options = help_text[help_text.index('positional arguments'):]
options = re.sub(r'^(\w.+)$', r'## \1', options, flags=re.MULTILINE)
options = re.sub(r'^  ', r'    ', options, flags=re.MULTILINE)
options = '# OPTIONS\n' + options + '\n'


with open('build/' + README_FILE, 'w') as output_file:
    output_file.write(header)
    output_file.write(options)
    output_file.write(footer)
