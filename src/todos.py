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

COMMENTS = ['#', '//', '/*']
PATTERNS = [r'\bTODO\b', r'\bFIXME\b']
SUPPRESSED = ['.git', '.svn', 'CVS']
DIRECTORIES = ['.']
NUM_LINES = 1


###############################################################################
####

class Comment:
	def __init__(self, pattern, file, pos, lines):
		self.pattern = pattern
		self.file = file
		self.pos = pos
		self.lines = lines


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
		self.parameters = parameters
		self.comments = []

		if self.parameters.extensions is not None:
			self.parameters.extensions = ['.' + e for e in self.parameters.extensions]

		flags = 0
		if self.parameters.ignoreCase:
			flags = re.IGNORECASE

		self.parameters.compiledPatterns = []
		for pattern in self.parameters.patterns:
			try:
				self.parameters.compiledPatterns.append(Pattern(pattern, re.compile(pattern, flags)))
			except re.error as e:
				print >> sys.stderr, 'Pattern compilation failed:', pattern + ',', e


	def dumpConfiguration(self):
		self.verbose('Command line arguments:')
		self.verbose('verbose: ' + str(self.parameters.verbose))
		self.verbose('comments: ' + str(self.parameters.comments))
		self.verbose('patterns: ' + str(self.parameters.patterns))
		self.verbose('extensions: ' + str(self.parameters.extensions))
		self.verbose('suppressed-dirs: ' + str(self.parameters.suppressed))
		self.verbose('ignore-case: ' + str(self.parameters.ignoreCase))
		self.verbose('num-lines: ' + str(self.parameters.numLines))
		self.verbose('out-txt: ' + str(self.parameters.outTxt))
		self.verbose('out-xml: ' + str(self.parameters.outXml))
		self.verbose('out-html: ' + str(self.parameters.outHtml))
		self.verbose('force: ' + str(self.parameters.force))
		self.verbose('directories: ' + str(self.parameters.directories))
		self.verbose('')


	def search(self):
		self.processDirectories()


	def verbose(self, message):
		if self.parameters.verbose:
			print message


	def processDirectories(self):
		for directory in self.parameters.directories:
			self.processDirectory(directory, directory)


	def isDirectorySuppressed(self, directory, dirName):
		if self.parameters.suppressed is None:
			return False

		return dirName in self.parameters.suppressed


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
		if self.parameters.extensions is None:
			return True

		for extension in self.parameters.extensions:
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


	def containsComment(self, line):
		for comment in self.parameters.comments:
			if line.count(comment) > 0:
				return True

		return False


	def processLine(self, file, pos, line, lines):
		if not self.containsComment(line):
			return

		for pattern in self.parameters.compiledPatterns:
			if pattern.rePattern.search(line):
				self.comments.append(Comment(pattern.pattern, file, pos,
						self.getLines(lines, pos-1, self.parameters.numLines)))
				break


	def getLines(self, lines, pos, num):
		lastLine = pos+num
		if lastLine >= len(lines):
			lastLine = len(lines)

		result = []
		for i in range(pos, lastLine):
			result.append(lines[i].rstrip())

		return result


	def output(self):
		self.writeTxt()
		self.writeXml()
		self.writeHtml()


	def writeTxt(self):
		if self.parameters.outTxt is None:
			return

		self.verbose('Writing TXT output: ' + self.parameters.outTxt)

		if self.parameters.outTxt == 'stdout':
			outFile = sys.stdout
		else:
			if os.path.exists(self.parameters.outTxt) and not self.parameters.force:
				print >> sys.stderr, 'File exists, use force parameter to override:', self.parameters.outTxt
				return

			try:
				outFile = open(self.parameters.outTxt, 'w')
			except IOError, e:
				print >> sys.stderr, 'Opening file failed:', e
				return

		if self.parameters.numLines > 1:
			print >> outFile, '--'

		for comment in self.comments:
			pos = comment.pos

			for line in comment.lines:
				print >> outFile,  comment.file + ':' + str(pos), line
				pos += 1

			if self.parameters.numLines > 1:
				print >> outFile, '--'

		if self.parameters.outTxt != 'stdout':
			outFile.close()


	def writeXml(self):
		if self.parameters.outXml is None:
			return

		self.verbose('Writing XML output: ' + self.parameters.outXml)
		# FIXME: add implementation
		pass


	def writeHtml(self):
		if self.parameters.outHtml is None:
			return

		self.verbose('Writing HTML output: ' + self.parameters.outHtml)
		# FIXME: add implementation
		pass


###############################################################################
####

def parseCommandLineArguments():
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
			'-c', '--comment',
			nargs='+',
			help='the comment characters',
			metavar='COMMENT',
			dest='comments',
			default=COMMENTS)

	parser.add_argument(
			'-e', '--regexp',
			nargs='+',
			help="the pattern to search; see Python's re module for proper syntax",
			metavar='PATTERN',
			dest='patterns',
			default=PATTERNS)

	parser.add_argument(
			'-A', '--after-context',
			type=int,
			metavar='NUM',
			dest='numLines',
			help='number of lines that are sent to the output together with the matching line',
			default=NUM_LINES)

	parser.add_argument(
			'-t', '--file-ext',
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
			'-o', '--out-txt',
			nargs='?',
			const='stdout',
			metavar='TXT',
			dest='outTxt',
			help='the output text file; standard output will be used if the path is not specified')

	parser.add_argument(
			'-x', '--out-xml',
			metavar='XML',
			dest='outXml',
			help='the output XML file')

	parser.add_argument(
			'-m', '--out-html',
			metavar='HTML',
			dest='outHtml',
			help='the output HTML file')

	parser.add_argument(
			'-f', '--force',
			action='store_true',
			default=False,
			help='override existing output files')

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
	commentsSearch.output()


###############################################################################
####

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
