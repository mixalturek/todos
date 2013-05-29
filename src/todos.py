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
#### Configuration, default values

VERSION = '0.1.0'

PATTERNS = ['TODO', 'FIXME']
SUPPRESSED = ['.git', '.svn', 'CVS']
DIRECTORIES = ['.']


###############################################################################
####

class Comment:
	def __init__(self, pattern, file, pos, lines):
		self.pattern = pattern
		self.file = file
		self.pos = pos
		self.lines = lines

	def __str__(self):
		fileLine = self.file + ':' + str(self.pos) + ': '

		if len(self.lines) == 1:
			return fileLine + self.lines[0]
		else:
			result = ""

			for line in self.lines:
				result += fileLine + line

			return result


###############################################################################
####

class Pattern:
	def __init__(self, pattern, rePattern):
		self.pattern = pattern
		self.rePattern = rePattern


	def __str__(self):
		return self.pattern


###############################################################################
####

class CommentsSearch:
	def __init__(self, parameters):
		self.__parameters = parameters
		self.__comments = []

		if self.__parameters.extensions is not None:
			self.__parameters.extensions = ['.' + e for e in self.__parameters.extensions]

		if self.__parameters.ignoreCase:
			self.__parameters.compiledPatterns = [Pattern(pattern, re.compile(pattern, re.IGNORECASE))
					for pattern in self.__parameters.patterns]
		else:
			self.__parameters.compiledPatterns = [Pattern(pattern, re.compile(pattern))
					for pattern in self.__parameters.patterns]


	def dumpConfiguration(self):
		self.verbose('Command line arguments:')
		self.verbose('verbose: ' + str(self.__parameters.verbose))
		self.verbose('patterns: ' + str(self.__parameters.patterns))
		self.verbose('extensions: ' + str(self.__parameters.extensions))
		self.verbose('suppressed-dirs: ' + str(self.__parameters.suppressed))
		self.verbose('ignore-case: ' + str(self.__parameters.ignoreCase))
		self.verbose('num-lines: ' + str(self.__parameters.numLines))
		self.verbose('txt: ' + str(self.__parameters.txt))
		self.verbose('xml: ' + str(self.__parameters.xml))
		self.verbose('html: ' + str(self.__parameters.html))
		self.verbose('directories: ' + str(self.__parameters.directories))
		self.verbose('')


	def search(self):
		self.processDirectories()


	def verbose(self, message):
		if self.__parameters.verbose:
			print(message)


	def processDirectories(self):
		for directory in self.__parameters.directories:
			self.processDirectory(directory, directory)


	def isDirectorySuppressed(self, directory, dirName):
		if self.__parameters.suppressed is None:
			return False

		return dirName in self.__parameters.suppressed


	def processDirectory(self, directory, dirName):
		'''
		Recursively search files in specified directories.

		:param directory: the directory to search the files in
		'''

		if not os.path.isdir(directory):
			self.verbose('Skipping directory (not a directory): ' + directory)
			return

		if self.isDirectorySuppressed(directory, dirName):
			self.verbose('Skipping directory (suppressed): ' + directory)
			return

		for item in os.listdir(directory):
			path = os.path.join(directory, item)

			if os.path.isfile(path):
				self.processFile(path)
			else:
				self.processDirectory(path, item)


	def isFileExtensionAllowed(self, file):
		if self.__parameters.extensions is None:
			return True

		for extension in self.__parameters.extensions:
			if file.endswith(extension):
				return True

		return False


	def processFile(self, file):
		if not self.isFileExtensionAllowed(file):
			self.verbose('Skipping file (file extension): ' + file)
			return

		self.verbose('Parsing file: ' + file)

		try:
			with open(file, 'r') as f:
				lines = f.readlines()

			pos = 0
			for line in lines:
				pos += 1
				self.processLine(file, pos, line, lines)
		except UnicodeError:
			self.verbose('Skipping file (unicode error): ' + file)


	def processLine(self, file, pos, line, lines):
		for pattern in self.__parameters.compiledPatterns:
			if pattern.rePattern.search(line):
				self.__comments.append(Comment(pattern.pattern, file, pos,
						self.getLines(lines, pos-1, self.__parameters.numLines)))
				break


	def getLines(self, lines, pos, num):
		lastLine = pos+num
		if lastLine >= len(lines):
			lastLine = len(lines)

		result = []
		for i in range(pos, lastLine):
			result.append(lines[i])

		return result


	# TODO: debug
	def dumpComments(self):
		for comment in self.__comments:
			print(str(comment).rstrip())
			if self.__parameters.numLines > 1:
				print '--'


###############################################################################
####

def parseCommandLineArguments():
	patterns = ['TODO', 'FIXME']
	suppressed = ['.git', '.svn', 'CVS']
	directories = ['.']
	numLines = 1

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
			default=False)

	parser.add_argument(
			'-e', '--regexp',
			nargs='+',
			help='the pattern to search',
			metavar='PATTERN',
			dest='patterns',
			default=PATTERNS)

	parser.add_argument(
			'-A', '--after-context',
			type=int,
			metavar='NUM',
			dest='numLines',
			help='print %(metavar)s lines of trailing context after matching line',
			default=numLines)

	parser.add_argument(
			'-f', '--file-ext',
			metavar='EXT',
			nargs='+',
			help='check only files with the specified extension',
			dest='extensions')

	parser.add_argument(
			'-D', '--suppressed',
			metavar='DIR',
			nargs='+',
			help='suppress the specified directory',
			default=SUPPRESSED)

	parser.add_argument(
			'-i', '--ignore-case',
			action='store_true',
			help='ignore case distinctions',
			dest='ignoreCase',
			default=False)

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
			# ValueError: dest supplied twice for positional argument
			# dest='directories',
			default=DIRECTORIES)

	parameters = parser.parse_args()

	# Workaround for ValueError: dest supplied twice for positional argument
	parameters.directories = parameters.directory

	return parameters


###############################################################################
####

def main():
	commentsSearch = CommentsSearch(parseCommandLineArguments())
	commentsSearch.dumpConfiguration()
	commentsSearch.search()

	# TODO: debug
	commentsSearch.dumpComments()


###############################################################################
####

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
