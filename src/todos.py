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


import argparse
import os
import os.path
import sys
import re


###############################################################################
####

VERSION = '0.1.0'


###############################################################################
####

class Comment:
	def __init__(self, pattern, file, pos, line):
		self.__pattern = pattern
		self.__file = file
		self.__pos = pos
		self.__line = line.strip()


	def __str__(self):
		return self.__file + ':' + str(self.__pos) + ': ' + self.__line


###############################################################################
####

class CommentsSearch:
	def __init__(self, parameters):
		self.__parameters = parameters
		self.__comments = []


	def search(self):
		files = []
		for directory in self.__parameters.directory:
			self.processDirectory(directory)


	def processDirectory(self, directory):
		'''
		Recursively search files in specified directories.

		:param directory: the directory to search the files in
		'''

		# FIXME: verify it is a directory

		for item in os.listdir(directory):
			path = os.path.join(directory, item)

			if os.path.isfile(path):
				# TODO: check extension
				self.processFile(path)
			elif os.path.isdir(path) and item not in self.__parameters.excludeDirs:
				self.processDirectory(path)


	def processFile(self, file):
		if self.__parameters.verbose:
			print('Parsing file: ' + file)

		try:
			with open(file, 'r') as f:
				lines = f.readlines()

			pos = 0
			for line in lines:
				++pos
				self.processLine(file, pos, line)
		except UnicodeError:
			if self.__parameters.verbose:
				print('Skipping file: ' + file)


	def processLine(self, file, pos, line):
		for pattern in self.__parameters.patterns:
			# TODO: ignore case
			if re.search(pattern, line):
				self.__comments.append(Comment(pattern, file, pos, line))
				break


	# TODO: remove
	def dumpComments(self):
		for comment in self.__comments:
			print(str(comment))


###############################################################################
####

def main():
	patterns = ['TODO', 'FIXME']
	excludeDirs = ['.git', '.svn', 'CVS']

	parser = argparse.ArgumentParser(
		prog='todos',
		description='Search project directory for TODO, FIXME and similar comments.',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument(
			'-V', '--version',
			help='show version and exit',
			action='version',
			version='%(prog)s ' + VERSION)

	parser.add_argument(
			'-v', '--verbose',
			help='increase output verbosity',
			action='store_true',
			default=0)

	parser.add_argument(
			'-p', '--pattern',
			nargs='+',
			help='the search patterns',
			dest='patterns',
			default=patterns)

	parser.add_argument(
			'-f', '--file-ext',
			metavar='EXT',
			nargs='+',
			help='check only files with the specified extension',
			dest='extensions')

	parser.add_argument(
			'-D', '--exclude-dir',
			metavar='DIR',
			nargs='+',
			help='exclude the specified directories',
			dest='excludeDirs',
			default=excludeDirs)

	parser.add_argument(
			'-t', '--txt',
			nargs='?',
			help='the output text file; standard output will be used if the path is not specified')

	parser.add_argument(
			'-x', '--xml',
			nargs=1,
			help='the output XML file')

	parser.add_argument(
			'-m', '--html',
			nargs=1,
			help='the output HTML file')

	parser.add_argument(
			'directory',
			nargs='*',
			help='the input directory to search in',
			default='.')

	parameters = parser.parse_args()

	# TODO: remove
	if parameters.verbose:
		print 'Command line parameters:'
		print '\tverbose:', parameters.verbose
		print '\tpatterns:', parameters.patterns
		print '\textensions:', parameters.extensions
		print '\texclude-dirs:', parameters.excludeDirs
		print '\ttxt:', parameters.txt
		print '\txml:', parameters.xml
		print '\thtml:', parameters.html
		# TODO: rename to directories somehow
		print '\tdirectories:', parameters.directory
		print


	commentsSearch = CommentsSearch(parameters)
	commentsSearch.search()

	# TODO: remove
	commentsSearch.dumpComments()


###############################################################################
####

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
