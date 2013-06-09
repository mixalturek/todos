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

class TxtFormatter:
	MULTILINE_DELIMITER = '--'


	def __init__(self, multiline):
		self.multiline = multiline


	def getType(self):
		return 'TXT'


	def writeHeader(self, outStream):
		# Empty
		pass


	def writeData(self, outStream, comments, summary):
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


	def writeData(self, outStream, comments, summary):
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

<title>Comments Report - todos</title>

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

table       { margin-top: 1.5em; max-width: 100%; }
th          { background-color: #AFB3CC; text-align: left; }
th, td      { vertical-align: top; padding: 0.2em 0.5em 0.2em 0.5em; }
tr          { background-color: #D0D0EE; }
tr:hover    { background-color: #C0C0FF; }

#footer     { font-size: 9pt; margin-top: 2em; border-top: 1px solid silver; color: gray; }
</style>

</head>

<body>

<h1>Comments Report</h1>
'''


	def writeData(self, outStream, comments, summary):
		print >> outStream, '<h2 id="toc">Table of Contents</h2>\n'
		self.writeToc(outStream)

		print >> outStream, '<h2 id="summary">Summary</h2>\n'

		print >> outStream, '<h3 id="general">General</h3>\n'
		self.writeGeneralSummary(outStream, summary)

		print >> outStream, '<h3 id="perPatterns">Per Patterns</h3>\n'
		self.writePerPattern(outStream, summary.perPattern)

		print >> outStream, '<h3 id="perFiles">Per Files</h3>\n'
		self.writePerFile(outStream, summary.perFile)

		print >> outStream, '<h2 id="details">Details</h2>\n'
		self.writeComments(outStream, comments)


	def writeToc(self, outStream):
		print >> outStream, '''
<ul>
<li><a href="#toc">Table of Contents</a></li>
<li><a href="#summary">Summary</a>
	<ul>
	<li><a href="#general">General</a></li>
	<li><a href="#perPatterns">Per Patterns</a></li>
	<li><a href="#perFiles">Per Files</a></li>
	</ul>
</li>
<li><a href="#details">Details</a></li>
</ul>
'''


	def writeGeneralSummary(self, outStream, summary):
		numFilesWithMatches = 0
		for file, count in summary.perFile.iteritems():
			if count != 0:
				numFilesWithMatches += 1

		rows = [['Searched Patterns', len(summary.perPattern)],
				['Files with Matches', numFilesWithMatches],
				['Total Files', summary.totalFiles],
				['Total Directories', summary.totalDirectories]]
		self.htmlTable(outStream, ['Parameter', 'Value'], rows)


	def writePerPattern(self, outStream, perPattern):
		rows = [[self.htmlSpecialChars(p), c] for p, c in perPattern.iteritems()]
		rows.sort(key=itemgetter(1), reverse=True)
		self.htmlTable(outStream, ['Pattern', 'Occurrences'], rows)


	def writePerFile(self, outStream, perFile):
		rows = []

		for file, count in perFile.iteritems():
			if count != 0:
				# FIXME: The link should be relative to the output directory
				rows.append(['<a href="{0}">{0}</a>'.format(self.htmlSpecialChars(file)), count])

		rows.sort(key=itemgetter(1), reverse=True)
		self.htmlTable(outStream, ['File', 'Occurrences'], rows)


	def writeComments(self, outStream, comments):
		rows = []

		for comment in comments:
			# FIXME: The link should be relative to the output directory
			file = self.htmlLink(comment.file)
			pattern = self.htmlSpecialChars(comment.pattern)
			content = '<pre>{0}</pre>'.format(self.htmlSpecialChars('\n'.join(comment.lines)))
			rows.append([file, comment.pos, pattern, content])

		self.htmlTable(outStream, ['File', 'Line', 'Pattern', 'Content'], rows)


	def writeFooter(self, outStream):
		print >> outStream, '<p id="footer">Page generated: {0}, <a href="http://todos.sourceforge.net/">todos</a>  {1}.</p>'.format(strftime("%Y-%m-%d %H:%M:%S", localtime()), TODOS_VERSION)
		print >> outStream, '</body>'
		print >> outStream, '</html>'


	def htmlSpecialChars(self, text):
		ret = text
		ret = ret.replace('&', '&amp;')
		ret = ret.replace('"', '&quot;')
		ret = ret.replace('<', '&lt;')
		ret = ret.replace('>', '&gt;')
		return ret


	def htmlLink(self, destination):
		return '<a href="{0}">{0}</a>'.format(self.htmlSpecialChars(destination))


	def htmlTable(self, outStream, headers, rows):
		print >> outStream, '<table>\n<thead>\n<tr>'

		for header in headers:
			print >> outStream, '<th>{0}</th>'.format(header)

		print >> outStream, '</tr>\n</thead>\n\n<tbody>\n'

		for row in rows:
			print >> outStream, '<tr>'

			for item in row:
				print >> outStream, '<td>{0}</td>'.format(item)

			print >> outStream, '</tr>\n'


		print >> outStream, '</tbody>\n</table>\n'


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

class Summary:
	def __init__(self, parameters):
		self.totalFiles = 0
		self.totalDirectories = 0

		self.perPattern = {}
		self.perFile = {}

		for pattern in parameters.patterns:
			self.perPattern[pattern] = 0


###############################################################################
####

class CommentsSearch:
	def __init__(self, parameters):
		self.parameters = parameters
		self.comments = []
		self.summary = Summary(parameters)

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

		self.summary.totalDirectories += 1

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


	def isFileBinary(self, file):
		CHUNK_SIZE = 1024

		try:
			with open(file, 'rb') as f:
				chunk = f.read(CHUNK_SIZE)
		except IOError as e:
			print >> sys.stderr, 'Reading from file failed:', e
			return True

		# If the begin of the file contains a null byte, guess that the file is binary.
		# GNU grep works similarly, see file_is_binary() in its source codes.
		#
		# The following works nicely for common ascii/utf8 encoded source codes
		# with binary object files, images and jar packages in the same directory tree.
		# The heuristic can be extended in future if needed,
		#
		# Note UTF-16 encoded text files will be clasified as binary, is it correct/incorrect?
		return '\0' in chunk


	def processFile(self, file):
		if not self.isFileExtensionAllowed(file):
			self.verbose('Skipping file (file extension): ' + file)
			return

		if self.isFileBinary(file):
			self.verbose('Skipping file (binary file): ' + file)
			return

		self.verbose('Parsing file: ' + file)

		try:
			with open(file, 'r') as f:
				lines = f.readlines()

			self.summary.totalFiles += 1
			self.summary.perFile[file] = 0

			pos = 0
			for line in lines:
				pos += 1
				self.processLine(file, pos, line, lines)
		except IOError as e:
			print >> sys.stderr, 'Reading from file failed:', e
		except UnicodeError as e:
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
				self.summary.perPattern[pattern.pattern] += 1
				self.summary.perFile[file] += 1
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
		formatter.writeData(outStream, self.comments, self.summary)
		formatter.writeFooter(outStream)


	def outputDataToFile(self, path, formatter):
		self.verbose('Writing {0} output: {1}'.format(formatter.getType(), path))

		if os.path.exists(path) and not self.parameters.force:
			print >> sys.stderr, 'File exists, use force parameter to override:', path
			return

		try:
			with open(path, 'w') as outStream:
				self.outputData(outStream, formatter)
		except IOError as e:
			print >> sys.stderr, 'Output failed:', e
			return


###############################################################################
####

class Todos:
	def __init__(self):
		pass


	def parseCommandLineArguments(self, argv):
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

		parameters = parser.parse_args(argv)

		# Workaround for ValueError: dest supplied twice for positional argument
		parameters.directories = parameters.directory

		return parameters


	def dumpConfigurationIfVerbose(self, parameters):
		if not parameters.verbose:
			return

		print 'Command line arguments:'
		print 'verbose: ', parameters.verbose
		print 'comments: ', parameters.comments
		print 'patterns: ', parameters.patterns
		print 'extensions: ', parameters.extensions
		print 'suppressed-dirs: ', parameters.suppressed
		print 'ignore-case: ', parameters.ignoreCase
		print 'num-lines: ', parameters.numLines
		print 'out-txt: ', parameters.outTxt
		print 'out-xml: ', parameters.outXml
		print 'out-html: ', parameters.outHtml
		print 'force: ', parameters.force
		print 'directories: ', parameters.directories
		print ''


	def main(self, argv):
		parameters = self.parseCommandLineArguments(argv)
		self.dumpConfigurationIfVerbose(parameters)

		commentsSearch = CommentsSearch(parameters)
		commentsSearch.search()
		commentsSearch.output()


###############################################################################
####

if __name__ == '__main__':
	try:
		todos = Todos()
		todos.main(sys.argv[1:])
	except KeyboardInterrupt as e:
		sys.exit('\nERROR: Interrupted by user')
