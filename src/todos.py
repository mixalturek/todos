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

TODOS_VERSION = '0.1.0'
XML_VERSION = '0.1.0'

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

# TODO: summary in TXT

class TxtFormatter:
	MULTILINE_DELIMITER = '--'


	def __init__(self, multiline):
		self.multiline = multiline


	def getType(self):
		return 'TXT'


	def writeHeader(self, outStream):
		# Empty
		pass


	def writeComments(self, outStream, comments):
		if self.multiline:
			print >> outStream, self.MULTILINE_DELIMITER

		for comment in comments:
			pos = comment.pos

			for line in comment.lines:
				print >> outStream, '{0}:{1}: {2}'.format(comment.file, pos, line)
				pos += 1

			if self.multiline:
				print >> outStream, self.MULTILINE_DELIMITER


	def writeFooter(self, outStream):
		# Empty
		pass


###############################################################################
####

# TODO: summary in XML

class XmlFormatter:
	def __init__(self):
		# Empty
		pass


	def getType(self):
		return 'XML'


	def writeHeader(self, outStream):
		print >> outStream, '<?xml version="1.0" encoding="utf-8" standalone="yes"?>'
		print >> outStream, '<Todos>'
		print >> outStream, '\t<Version todos="{0}" format="{1}">'.format(TODOS_VERSION, XML_VERSION)
		print >> outStream, '\t<Comments>'


	def writeComments(self, outStream, comments):
		for comment in comments:
			print >> outStream, '\t\t<Comment pattern="{0}" file="{1}" line="{2}">'.format(
					self.xmlSpecialChars(comment.pattern),
					self.xmlSpecialChars(comment.file),
					comment.pos)

			for line in comment.lines:
				print >> outStream, '\t\t\t{0}'.format(self.xmlSpecialChars(line))

			print >> outStream, '\t\t</Comment>'


	def writeFooter(self, outStream):
		print >> outStream, '\t</Comments>'
		print >> outStream, '</Todos>'


	def xmlSpecialChars(self, text):
		ret = text
		ret = ret.replace('&', '&amp;')
		ret = ret.replace('"', '&quot;')
		ret = ret.replace('<', '&lt;')
		ret = ret.replace('>', '&gt;')
		return ret


###############################################################################
####

# TODO: summary in HTML

class HtmlFormatter:
	def __init__(self):
		# Empty
		pass


	def getType(self):
		return 'HTML'


	def writeHeader(self, outStream):
		print >> outStream, '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8" />
<meta http-equiv="content-language" content="en" />

<title>Comments - todos</title>

<style type="text/css" media="all">
* { margin: 0; padding: 0; }

body
{
	margin: 2em; padding: 0px;
	background-color: white; color: black;
	font-family: Verdana, "Bitstream Vera Sans", Geneva, Arial, sans-serif;
	font-size: 10pt; line-height: 1.6em;
}

pre         { line-height: 1.1em; margin: 0; margin: 0.2em 0 0.2em 0; }
a:hover     { color: blue; }

table       { margin-top: 1.5em; max-width: 100%; }
th          { background-color: #AFB3CC; }
th, td      { vertical-align: top; padding: 0.2em 0.5em 0.2em 0.5em; }
tr          { background-color: #D0D0EE; }
tr:hover    { background-color: #C0C0FF; }

#footer     { font-size: 9pt; margin-top: 3em; border-top: 1px solid silver; color: gray; }
</style>

</head>

<body>

<h1>Comments</h1>
'''


	def writeComments(self, outStream, comments):
		print >> outStream, '<table>'
		print >> outStream, '<thead>'
		print >> outStream, '<tr>'
		print >> outStream, '<th>File</th>'
		print >> outStream, '<th>Line</th>'
		print >> outStream, '<th>Pattern</th>'
		print >> outStream, '<th>Content</th>'
		print >> outStream, '</tr>'
		print >> outStream, '</thead>'
		print >> outStream, '<tbody>'
		print >> outStream

		for comment in comments:
			print >> outStream, '<tr>'
			print >> outStream, '<td><a href="{0}">{0}</a></td>'.format(self.htmlSpecialChars(comment.file))
			print >> outStream, '<td>{0}</td>'.format(comment.pos)
			print >> outStream, '<td>{0}</td>'.format(self.htmlSpecialChars(comment.pattern))
			print >> outStream, '<td><pre>'
			for line in comment.lines:
				print >> outStream, '{0}'.format(self.htmlSpecialChars(line))
			print >> outStream, '</pre></td>'
			print >> outStream, '</tr>'
			print >> outStream

		print >> outStream, '</tbody>'
		print >> outStream, '</table>'


	def writeFooter(self, outStream):
		print >> outStream, '<p id="footer">This page was generated using <a href="http://todos.sourceforge.net/">todos</a> tool.</p>'
		print >> outStream, '</body>'
		print >> outStream, '</html>'


	def htmlSpecialChars(self, text):
		ret = text
		ret = ret.replace('&', '&amp;')
		ret = ret.replace('"', '&quot;')
		ret = ret.replace('<', '&lt;')
		ret = ret.replace('>', '&gt;')
		return ret


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
		outputWritten = False

		if self.parameters.outTxt is not None:
			self.outputDataToFile(self.parameters.outTxt, TxtFormatter(self.parameters.numLines > 1))
			outputWritten = True

		if self.parameters.outXml is not None:
			self.outputDataToFile(self.parameters.outXml, XmlFormatter())
			outputWritten = True

		if self.parameters.outHtml is not None:
			self.outputDataToFile(self.parameters.outHtml, HtmlFormatter())
			outputWritten = True

		# Use stdout if no output method is specified explicitly
		if outputWritten == False:
			self.outputData(sys.stdout, TxtFormatter(self.parameters.numLines > 1))


	def outputData(self, outStream, formatter):
		formatter.writeHeader(outStream)
		formatter.writeComments(outStream, self.comments)
		formatter.writeFooter(outStream)


	def outputDataToFile(self, path, formatter):
		self.verbose('Writing {0} output: {1}'.format(formatter.getType(), path))

		if os.path.exists(path) and not self.parameters.force:
			print >> sys.stderr, 'File exists, use force parameter to override:', path
			return

		try:
			with open(path, 'w') as outStream:
				self.outputData(outStream, formatter)
		except IOError, e:
			print >> sys.stderr, 'Output failed:', e
			return


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
			version='%(prog)s ' + TODOS_VERSION)

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
