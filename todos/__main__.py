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

# Execute with
# $ python todos/__main__.py (python 2.6+)
# $ python -m todos          (python 2.7+)


import sys
#import todos
from todos.FilesSearch import FilesSearch
from todos.CommentsSearch import CommentsSearch


def main(argv):
	# TODO: parse command line arguments
	defaultPatterns = ['TODO', 'FIXME', '@[A-Z]{2,3}@']

	filesSearch = FilesSearch()
	files = filesSearch.search('.')

	commentsSearch = CommentsSearch(defaultPatterns)

	for file in files:
		# TODO: verbose only
		# print('Parsing: ' + file)
		try:
			commentsSearch.processFile(file)
		except UnicodeError:
			print('Skipped: ' + file)

	# TODO: remove
	commentsSearch.dumpComments()


if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
