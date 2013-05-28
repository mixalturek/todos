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


class Comment:
	def __init__(self, pattern, file, pos, line):
		self.__pattern = pattern
		self.__file = file
		self.__pos = pos
		self.__line = line.strip()


	def __str__(self):
		return self.__file + ":" + str(self.__pos) + ": " + self.__line


	def __repr__(self):
		return self.__str__()
