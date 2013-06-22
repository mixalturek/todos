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
Search TODO, FIXME and similar comments in project files.
"""


import argparse
import os
import os.path
import sys
import re
import socket
import codecs
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
ENCODING = 'utf-8'


###############################################################################
####

class Todos:
	"""
	Top level module class that contains enter to the application. It drives
	parsing of the input files, searching comments and output of the results.
	"""


	def __init__(self):
		"""
		Class constructor.
		"""

		self.logger = Logger(False) # Will be redefined in main()
		""" The logger used in the application. """


	def main(self, argv):
		"""
		Enter the application.
		"""
		parameters = self.parseCommandLineArguments(argv)
		self.logger = Logger(parameters.verbose)
		self.verifyParameters(parameters)
		self.dumpParameters(parameters)

		commentsSearch = CommentsSearch(parameters, self.logger)
		commentsSearch.search()

		outputWriter = OutputWriter(parameters, self.logger)
		outputWriter.output(commentsSearch)


	def parseCommandLineArguments(self, argv):
		"""
		Parse all command line arguments and return them in object form.
		"""
		parser = argparse.ArgumentParser(
				prog='todos',
				description='Search project directory for TODO, FIXME and similar comments.',
				formatter_class=argparse.ArgumentDefaultsHelpFormatter
		)

		parser.add_argument(
				'-V', '--version',
				help='show version and exit',
				action='version',
				version='%(prog)s ' + TODOS_VERSION
		)

		parser.add_argument(
				'-v', '--verbose',
				help='increase output verbosity',
				action='store_true',
				default=False
		)

		parser.add_argument(
				'-c', '--comment',
				nargs='+',
				help='the comment characters',
				metavar='COMMENT',
				dest='comments',
				default=COMMENTS
		)

		parser.add_argument(
				'-e', '--regexp',
				nargs='+',
				help="the pattern to search; see Python's re module for proper syntax",
				metavar='PATTERN',
				dest='patterns',
				default=PATTERNS
		)

		parser.add_argument(
				'-A', '--after-context',
				type=int,
				metavar='NUM',
				dest='numLines',
				help='number of lines that are sent to the output together with the matching line',
				default=NUM_LINES
		)

		parser.add_argument(
				'-t', '--file-ext',
				metavar='EXT',
				nargs='+',
				help='check only files with the specified extension',
				dest='extensions'
		)

		parser.add_argument(
				'-D', '--suppressed',
				metavar='DIR',
				nargs='+',
				help='suppress the specified directory',
				default=SUPPRESSED
		)

		parser.add_argument(
				'-n', '--encoding',
				help='the files encoding',
				default=ENCODING
		)

		parser.add_argument(
				'-i', '--ignore-case',
				action='store_true',
				help='ignore case distinctions',
				dest='ignoreCase',
				default=False
		)

		parser.add_argument(
				'-o', '--out-txt',
				metavar='TXT',
				dest='outTxt',
				help='the output text file; standard output will be used if the path is not specified'
		)

		parser.add_argument(
				'-x', '--out-xml',
				metavar='XML',
				dest='outXml',
				help='the output XML file'
		)

		parser.add_argument(
				'-m', '--out-html',
				metavar='HTML',
				dest='outHtml',
				help='the output HTML file'
		)

		parser.add_argument(
				'-f', '--force',
				action='store_true',
				default=False,
				help='override existing output files'
		)

		parser.add_argument(
				'directory',
				nargs='*',
				help='the input directory to search in',
				# ValueError: dest supplied twice for positional argument
				# dest='directories',
				default=DIRECTORIES
		)

		parameters = parser.parse_args(argv)

		# Workaround for ValueError: dest supplied twice for positional argument
		parameters.directories = parameters.directory

		return parameters


	def dumpParameters(self, parameters):
		"""
		Dump values of parameters if a verbose output is enabled.
		"""
		self.logger.verbose('Command line arguments:')
		self.logger.verbose(' '.join(sys.argv))
		self.logger.verbose('')

		self.logger.verbose('Parsed command line arguments:')
		self.logger.verbose('verbose: {0}'.format(parameters.verbose))
		self.logger.verbose('comments: {0}'.format(parameters.comments))
		self.logger.verbose('patterns: {0}'.format(parameters.patterns))
		self.logger.verbose('extensions: {0}'.format(parameters.extensions))
		self.logger.verbose('suppressed-dirs: {0}'.format(parameters.suppressed))
		self.logger.verbose('encoding: {0}'.format(parameters.encoding))
		self.logger.verbose('ignore-case: {0}'.format(parameters.ignoreCase))
		self.logger.verbose('num-lines: {0}'.format(parameters.numLines))
		self.logger.verbose('out-txt: {0}'.format(parameters.outTxt))
		self.logger.verbose('out-xml: {0}'.format(parameters.outXml))
		self.logger.verbose('out-html: {0}'.format(parameters.outHtml))
		self.logger.verbose('force: {0}'.format(parameters.force))
		self.logger.verbose('directories: {0}'.format(parameters.directories))
		self.logger.verbose('')


	def verifyParameters(self, parameters):
		"""
		Verify values of the input parameters.
		"""
		try:
			codecs.lookup(parameters.encoding)
		except LookupError as e:
			self.logger.warn('Encoding error: {0}'.format(e))
			self.logger.warn('Changing encoding to default: {0}'.format(ENCODING))
			parameters.encoding = ENCODING


###############################################################################
####

class Logger:
	"""
	A simple logger class.
	"""


	def __init__(self, verboseEnabled):
		"""
		Class constructor.
		"""
		self.verboseEnabled = verboseEnabled
		""" Flag to enable the verbose mode. """


	def verbose(self, message):
		"""
		Output a verbose message to the standard output stream if verbose mode
		is enabled.
		"""
		if self.verboseEnabled:
			print message


	def warn(self, message):
		"""
		Output a warning message to the standard error stream.
		"""
		print >> sys.stderr, 'WARN:', message


	def error(self, message):
		"""
		Output an error message to the standard error stream.
		"""
		print >> sys.stderr, 'ERROR:', message


###############################################################################
####

class Comment:
	"""
	Container to store one comment that was found.
	"""

	def __init__(self, pattern, file, pos, lines):
		"""
		Class constructor, initialize all members.
		"""
		self.pattern = pattern
		""" The pattern that was found. """

		self.file = file
		""" The input file. """

		# TODO: rename to position
		self.pos = pos
		""" The position in the file. """

		self.lines = lines
		""" The matching line and optionally several lines after it. """


###############################################################################
####

class Pattern:
	"""
	Container to store one pattern (regular expression) for searching.
	"""


	def __init__(self, pattern, rePattern):
		"""
		Class constructor, initialize all members.
		"""
		# TODO: rename pattern variable
		self.pattern = pattern
		""" The string representation of the pattern. """

		self.rePattern = rePattern
		""" The precompiled pattern. """


	def __str__(self):
		"""
		Return a string representation of the pattern.
		"""
		return self.pattern


###############################################################################
####

class Summary:
	"""
	Container to store a summary of the comments searching.
	"""

	def __init__(self, parameters):
		"""
		Class constructor, initialize all members to zero or empty list.
		"""
		self.totalFiles = 0
		""" The number of the examined files. """

		self.totalDirectories = 0
		""" The number of the examined directories. """

		self.perPattern = {}
		""" Summary per pattern. """

		self.perFile = {}
		""" Summary per file. """

		for pattern in parameters.patterns:
			self.perPattern[pattern] = 0


###############################################################################
####

class CommentsSearch:
	"""
	Search comments in the source files.
	"""

	def __init__(self, parameters, logger):
		"""
		Class constructor, prepare the object for searching.
		"""
		self.parameters = parameters
		""" The input parameters. """

		self.logger = logger
		""" The logger to output messages. """

		self.comments = []
		""" The comments that was found during the searching. """

		self.summary = Summary(parameters)
		""" The summary of the searching. """

		if self.parameters.extensions is not None:
			# TODO: append the dot only if it isn't already present
			self.parameters.extensions = ['.' + e for e in self.parameters.extensions]

		flags = 0
		if self.parameters.ignoreCase:
			flags = re.IGNORECASE

		self.parameters.compiledPatterns = []
		for pattern in self.parameters.patterns:
			try:
				self.parameters.compiledPatterns.append(Pattern(pattern, re.compile(pattern, flags)))
			except re.error as e:
				self.logger.warn('Pattern compilation failed: {0}, {1}'.format(pattern, e))


	def search(self):
		"""
		Recursively search the comments according to the input parameters.
		"""
		self.processDirectories()


	def processDirectories(self):
		"""
		Process all directories.
		"""
		for directory in self.parameters.directories:
			self.processDirectory(directory, directory)


	def isDirectorySuppressed(self, directory, dirName):
		"""
		Return true if the input directory should be skipped, otherwise false.
		"""
		if self.parameters.suppressed is None:
			return False

		return dirName in self.parameters.suppressed


	def processDirectory(self, directory, dirName):
		'''
		Recursively search files in the input directory.
		'''
		if not os.path.isdir(directory):
			self.logger.verbose('Skipping directory (not a directory): {0}'.format(directory))
			return

		if self.isDirectorySuppressed(directory, dirName):
			self.logger.verbose('Skipping directory (suppressed): {0}'.format(directory))
			return

		self.summary.totalDirectories += 1

		for item in os.listdir(directory):
			path = os.path.join(directory, item)

			if os.path.isfile(path):
				self.processFile(path)
			else:
				self.processDirectory(path, item)


	def isFileExtensionAllowed(self, file):
		"""
		Return true if the input file should be processed, otherwise false.
		"""
		if self.parameters.extensions is None:
			return True

		for extension in self.parameters.extensions:
			if file.endswith(extension):
				return True

		return False


	def isFileBinary(self, file):
		"""
		Return true if the input file is considered as binary, otherwise false.
		Note the return value may be incorrect, only beginning of the file is
		examined for '\0' character.
		"""
		CHUNK_SIZE = 1024

		try:
			with open(file, 'rb') as f:
				chunk = f.read(CHUNK_SIZE)
		except IOError as e:
			self.logger.warn('Reading from file failed: {0}, {1}'.format(file, e))
			return True

		# If the beginning of the file contains a null byte, guess that the file is binary.
		# GNU grep works similarly, see file_is_binary() in its source codes.
		#
		# The following works nicely for common ascii/utf8 encoded source codes
		# with binary object files, images and jar packages in the same directory tree.
		# The heuristic can be extended in future if needed,
		#
		# Note UTF-16 encoded text files will be clasified as binary, is it correct/incorrect?
		return '\0' in chunk


	def processFile(self, file):
		'''
		Process all lines of the input file.
		'''
		if not self.isFileExtensionAllowed(file):
			self.logger.verbose('Skipping file (file extension): {0}'.format(file))
			return

		if self.isFileBinary(file):
			self.logger.verbose('Skipping file (binary file): {0}'.format(file))
			return

		self.logger.verbose('Parsing file: {0}'.format(file))

		try:
			with codecs.open(file, 'r', self.parameters.encoding) as f:
				lines = f.readlines()

			self.summary.totalFiles += 1
			self.summary.perFile[file] = 0

			pos = 0
			for line in lines:
				pos += 1
				self.processLine(file, pos, line, lines)
		except IOError as e:
			self.logger.warn('Reading from file failed: {0}, {1}'.format(file, e))
		except UnicodeError as e:
			self.logger.warn('Skipping file (unicode error): {0}'.format(file))


	def containsComment(self, line):
		"""
		Return true if the input line contains a comment, otherwise false.
		"""
		for comment in self.parameters.comments:
			if line.count(comment) > 0:
				return True

		return False


	def processLine(self, file, pos, line, lines):
		'''
		Process the input line, search comment with one of the specified patterns.
		'''
		if not self.containsComment(line):
			return

		for pattern in self.parameters.compiledPatterns:
			if pattern.rePattern.search(line):
				linesToStore = self.getLines(lines, pos-1, self.parameters.numLines)
				self.comments.append(Comment(pattern.pattern, file, pos, linesToStore))
				self.summary.perPattern[pattern.pattern] += 1
				self.summary.perFile[file] += 1
				break


	def getLines(self, lines, pos, num):
		'''
		Return content of the specified number of lines.
		'''
		lastLine = pos+num
		if lastLine >= len(lines):
			lastLine = len(lines)

		result = []
		for i in range(pos, lastLine):
			result.append(lines[i].rstrip())

		return result


###############################################################################
####

class OutputWriter:
	"""
	Write the results of the searching to the output files in specified formats.
	"""


	def __init__(self, parameters, logger):
		"""
		Class constructor.
		"""
		self.parameters = parameters
		""" The input parameters. """

		self.logger = logger
		""" The logger to output messages. """


	def output(self, commentsSearch):
		"""
		Determine which formats are requested and store them to the appropriate
		files. If no output file is specified, use the standard output stream.
		"""
		outputWritten = False

		self.logger.verbose('') # New line to split the output

		if self.parameters.outTxt is not None:
			self.outputDataToFile(self.parameters.outTxt, TxtFormatter(self.parameters.numLines > 1), commentsSearch)
			outputWritten = True

		if self.parameters.outXml is not None:
			self.outputDataToFile(self.parameters.outXml, XmlFormatter(self.parameters), commentsSearch)
			outputWritten = True

		if self.parameters.outHtml is not None:
			self.outputDataToFile(self.parameters.outHtml, HtmlFormatter(self.parameters), commentsSearch)
			outputWritten = True

		# Use stdout if no output method is explicitly specified
		if outputWritten == False:
			self.outputData(sys.stdout, TxtFormatter(self.parameters.numLines > 1), commentsSearch)


	def outputDataToFile(self, path, formatter, commentsSearch):
		"""
		Open the output file and write the data.
		"""
		self.logger.verbose('Writing {0} output: {1}'.format(formatter.getType(), path))

		if os.path.exists(path) and not self.parameters.force:
			self.logger.warn('File exists, use force parameter to override: {0}'.format(file))
			return

		try:
			with codecs.open(path, 'w', self.parameters.encoding) as outStream:
				self.outputData(outStream, formatter, commentsSearch)
		except IOError as e:
			self.logger.error('Output failed: {0}, {1}'.format(file, e))
			return


	def outputData(self, outStream, formatter, commentsSearch):
		"""
		Output the data to the opened stream and use the specified formatter.
		"""
		formatter.writeHeader(outStream)
		formatter.writeData(outStream, commentsSearch.comments, commentsSearch.summary)
		formatter.writeFooter(outStream)


###############################################################################
####

class TxtFormatter:
	"""
	Text formatter.
	"""

	MULTILINE_DELIMITER = '--'
	""" Delimiter if multiline output is enabled. """


	def __init__(self, multiline):
		"""
		Class constructor.
		"""
		self.multiline = multiline
		""" Multiple lines per pattern will be passed to the output. """


	def getType(self):
		"""
		Return type of the formatter.
		"""
		return 'TXT'


	def writeHeader(self, outStream):
		"""
		Write the header to the output stream.
		"""
		# Empty
		pass


	def writeData(self, outStream, comments, summary):
		"""
		Write the data to the output stream.
		"""
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
		"""
		Write the footer to the output stream.
		"""
		# Empty
		pass


###############################################################################
####

# TODO: summary in XML

class XmlFormatter:
	"""
	XML formatter.
	"""


	def __init__(self, parameters):
		"""
		Class constructor.
		"""
		self.parameters = parameters
		""" The input parameters. """


	def getType(self):
		"""
		Return type of the formatter.
		"""
		return 'XML'


	def writeHeader(self, outStream):
		"""
		Write the header to the output stream.
		"""
		print >> outStream, '<?xml version="1.0" encoding="{0}" standalone="yes"?>'.format(self.parameters.encoding)
		print >> outStream, '<Todos>'
		print >> outStream, '\t<Version todos="{0}" format="{1}">'.format(TODOS_VERSION, XML_VERSION)
		print >> outStream, '\t<Comments>'


	def writeData(self, outStream, comments, summary):
		"""
		Write the data to the output stream.
		"""
		for comment in comments:
			print >> outStream, '\t\t<Comment pattern="{0}" file="{1}" line="{2}">'.format(
					self.xmlSpecialChars(comment.pattern),
					self.xmlSpecialChars(comment.file),
					comment.pos
			)

			for line in comment.lines:
				print >> outStream, '\t\t\t{0}'.format(self.xmlSpecialChars(line))

			print >> outStream, '\t\t</Comment>'


	def writeFooter(self, outStream):
		"""
		Write the footer to the output stream.
		"""
		print >> outStream, '\t</Comments>'
		print >> outStream, '</Todos>'


	def xmlSpecialChars(self, text):
		"""
		Replace all special characters by the XML entities and return a new string.
		"""
		ret = text
		ret = ret.replace('&', '&amp;')
		ret = ret.replace('"', '&quot;')
		ret = ret.replace('<', '&lt;')
		ret = ret.replace('>', '&gt;')
		return ret


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
		""" The input parameters. """


	def getType(self):
		"""
		Return type of the formatter.
		"""
		return 'HTML'


	def writeHeader(self, outStream):
		"""
		Write the header to the output stream.
		"""
		print >> outStream, '''<?xml version="1.0" encoding="{0}"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">

<head>
<meta http-equiv="content-type" content="text/html; charset={0}" />
<meta http-equiv="content-language" content="en" />
<title>Comments Report - todos</title>
'''.format(self.parameters.encoding)

		print >> outStream, '''
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
#sidebar    { position: fixed; top: 0px; left: 0px; width: 15%; padding: 2em; }
#footer     { font-size: 9pt; margin-top: 2em; border-top: 1px solid silver; color: gray; clear: both; }

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


	def writeData(self, outStream, comments, summary):
		"""
		Write the data to the output stream.
		"""
		print >> outStream, '<div id="sidebar">'

		self.writeToc(outStream)

		print >> outStream, '</div><!-- id="sidebar" -->'


		print >> outStream, '<div id="page">'

		print >> outStream, '<h1 id="commentsReport">Comments Report</h1>'

		print >> outStream, '<h2 id="inputParameters">Input Parameters</h2>\n'
		self.writeInputParameters(outStream)

		print >> outStream, '<h2 id="summary">Summary</h2>\n'

		print >> outStream, '<h3 id="general">General</h3>\n'
		self.writeGeneralSummary(outStream, summary)

		print >> outStream, '<h3 id="perPatterns">Per Patterns</h3>\n'
		self.writePerPattern(outStream, summary.perPattern)

		print >> outStream, '<h3 id="perFiles">Per Files</h3>\n'
		self.writePerFile(outStream, summary.perFile)

		print >> outStream, '<h2 id="details">Details</h2>\n'
		self.writeComments(outStream, comments)

		print >> outStream, '</div><!-- id="page" -->'


	def writeToc(self, outStream):
		"""
		Write table of contents as menu.
		"""
		print >> outStream, '''
<div class="menu_title">Menu</div>

<ul>
<li><a href="#commentsReport">Comments Report</a>
	<ul>
	<li><a href="#inputParameters">Input Parameters</a></li>
	<li><a href="#summary">Summary</a>
		<ul>
		<li><a href="#general">General</a></li>
		<li><a href="#perPatterns">Per Patterns</a></li>
		<li><a href="#perFiles">Per Files</a></li>
		</ul>
	</li>
	<li><a href="#details">Details</a></li>
	</ul>
</li>
</ul>
'''


	def writeInputParameters(self, outStream):
		"""
		Write input parameters as a table.
		"""
		rows = [['Computer', self.htmlSpecialChars(socket.gethostname())],
				['User', self.htmlSpecialChars(os.environ['LOGNAME'])],
				['Python', self.htmlSpecialChars('.'.join([str(v) for v in sys.version_info[0:3]]))],
		]
		self.htmlTable(outStream, ['Parameter', 'Value'], rows)

		print >> outStream, '<pre>'
		print >> outStream, 'cd {0}'.format(self.htmlSpecialChars(os.getcwd()))
		print >> outStream, self.htmlSpecialChars(' '.join(sys.argv))
		print >> outStream, '</pre>\n'

		rows = [['Working Directory', self.htmlSpecialChars(os.getcwd())],
				['Verbose', self.htmlSpecialChars(str(self.parameters.verbose))],
				['Comments', self.htmlSpecialChars(str(self.parameters.comments))],
				['Patterns', self.htmlSpecialChars(str(self.parameters.patterns))],
				['Extensions', self.htmlSpecialChars(str(self.parameters.extensions))],
				['Suppressed Directories', self.htmlSpecialChars(str(self.parameters.suppressed))],
				['Encoding', self.htmlSpecialChars(str(self.parameters.encoding))],
				['Ignore Case', self.htmlSpecialChars(str(self.parameters.ignoreCase))],
				['Number of Lines', self.htmlSpecialChars(str(self.parameters.numLines))],
				['Output TXT File', self.htmlSpecialChars(str(self.parameters.outTxt))],
				['Output XML File', self.htmlSpecialChars(str(self.parameters.outXml))],
				['Output HTML File', self.htmlSpecialChars(str(self.parameters.outHtml))],
				['Force', self.htmlSpecialChars(str(self.parameters.force))],
				['Directories', self.htmlSpecialChars(str(self.parameters.directories))],
		]
		self.htmlTable(outStream, ['Parameter', 'Value'], rows)


	def writeGeneralSummary(self, outStream, summary):
		"""
		Write summary as a table.
		"""
		numFilesWithMatches = 0
		for file, count in summary.perFile.iteritems():
			if count != 0:
				numFilesWithMatches += 1

		rows = [['Searched Patterns', len(summary.perPattern)],
				['Files with Matches', numFilesWithMatches],
				['Total Files', summary.totalFiles],
				['Total Directories', summary.totalDirectories]
		]
		self.htmlTable(outStream, ['Parameter', 'Value'], rows)


	def writePerPattern(self, outStream, perPattern):
		"""
		Write table of the input patterns together with the number of their occurrences.
		"""
		rows = [[self.htmlSpecialChars(p), c] for p, c in perPattern.iteritems()]
		rows.sort(key=itemgetter(1), reverse=True)
		self.htmlTable(outStream, ['Pattern', 'Occurrences'], rows)


	def writePerFile(self, outStream, perFile):
		"""
		Write table of the input files together with the number of the occurrences.
		Skip files with no occurrences.
		"""
		rows = []

		for file, count in perFile.iteritems():
			if count > 0:
				rows.append([self.htmlLink(os.path.abspath(file), file), count])

		rows.sort(key=itemgetter(1), reverse=True)
		self.htmlTable(outStream, ['File', 'Occurrences'], rows)


	def writeComments(self, outStream, comments):
		"""
		Write table of all occurrences with all details.
		"""
		rows = []

		for comment in comments:
			file = self.htmlLink(os.path.abspath(comment.file), comment.file)
			pattern = self.htmlSpecialChars(comment.pattern)
			content = '<pre>{0}</pre>'.format(self.htmlSpecialChars('\n'.join(comment.lines)))
			rows.append([file, comment.pos, pattern, content])

		self.htmlTable(outStream, ['File', 'Line', 'Pattern', 'Content'], rows)


	def writeFooter(self, outStream):
		"""
		Write the footer to the output stream.
		"""
		print >> outStream, '<p id="footer">Page generated: {0}, {1}, {2}.</p>'.format(
				strftime("%Y-%m-%d %H:%M:%S", localtime()),
				self.htmlLink('http://todos.sourceforge.net/', 'todos'),
				TODOS_VERSION
		)
		print >> outStream, '</body>'
		print >> outStream, '</html>'


	def htmlSpecialChars(self, text):
		"""
		Replace all special characters by the HTML entities and return a new string.
		"""
		ret = text
		ret = ret.replace('&', '&amp;')
		ret = ret.replace('"', '&quot;')
		ret = ret.replace('<', '&lt;')
		ret = ret.replace('>', '&gt;')
		return ret


	def htmlLink(self, target, text):
		"""
		Return a HTML link constructed from a target address and a label.
		"""
		return '<a href="{0}">{1}</a>'.format(
				self.htmlSpecialChars(target),
				self.htmlSpecialChars(text)
		)


	def htmlTable(self, outStream, headers, rows):
		"""
		Write a HTML table to the output stream.
		"""
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

if __name__ == '__main__':
	try:
		todos = Todos()
		todos.main(sys.argv[1:])
	except KeyboardInterrupt as e:
		sys.exit('\nERROR: Interrupted by user')
