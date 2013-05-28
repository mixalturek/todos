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


import unittest
from todos.FilesSearch import FilesSearch

class FilesSearchTestCase(unittest.TestCase):
	def test_search(self):
		filesSearch = FilesSearch()
		actual = filesSearch.search('./test_FilesSearch_data')
		self.assertEqual(2, len(actual))
		self.assertEqual(1, actual.count('./test_FilesSearch_data/file'))
		self.assertEqual(1, actual.count('./test_FilesSearch_data/subdir/file'))
