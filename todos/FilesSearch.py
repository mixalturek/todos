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
