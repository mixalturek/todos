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


import os
import os.path
import sys
import re


###############################################################################
####

class Comment:
	def __init__(self, pattern, file, pos, line):
		self.__pattern = pattern
		self.__file = file
		self.__pos = pos
		self.__line = line.strip()


	def __str__(self):
		return self.__file + ":" + str(self.__pos) + ": " + self.__line


###############################################################################
####

class CommentsSearch:
	def __init__(self, patterns):
		self.__patterns = patterns
		self.__comments = []


	def processFile(self, file):
		with open(file, 'r') as f:
			lines = f.readlines()

		pos = 0
		for line in lines:
			++pos
			self.processLine(file, pos, line)


	def processLine(self, file, pos, line):
		for pattern in self.__patterns:
			if re.search(pattern, line):
				self.__comments.append(Comment(pattern, file, pos, line))
				break


	# TODO: remove
	def dumpComments(self):
		for comment in self.__comments:
			print(str(comment))


###############################################################################
####

class FilesSearch:
	def __init__(self):
		pass


	def search(self, directory):
		"""
		Recursively search files in a directory.

		:param directory: the directory to search the files in
		:returns: the list of paths to the files relative to the input directory
		"""

		files = []

		for item in os.listdir(directory):
			path = os.path.join(directory, item)

			if os.path.isfile(path):
				files.append(path)
			elif os.path.isdir(path):
				files.extend(self.search(path))

		return files


###############################################################################
####

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
			# TODO: verbose only
			# print('Skipped: ' + file)
			pass

	# TODO: remove
	commentsSearch.dumpComments()


###############################################################################
####

if __name__ == '__main__':
	try:
		main(sys.argv)
	except KeyboardInterrupt:
		sys.exit('\nERROR: Interrupted by user')
