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


import re
from todos.Comment import Comment


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
