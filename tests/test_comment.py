#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Michal Turek
#
# This file is part of TODOs.
# http://todos.sourceforge.net/
#
# TODOs is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# TODOs is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with TODOs.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Unit test of Comment class.
"""


###############################################################################
####

import unittest
import todos.search


###############################################################################
####

class CommentTestCase(unittest.TestCase):
    def test_constructor(self):
        comment = todos.search.Comment('str_pattern', 'path', 42, ['line 1', 'line 2'])
        self.assertEqual('str_pattern', comment.str_pattern)
        self.assertEqual('path', comment.path)
        self.assertEqual(42, comment.position)
        self.assertEqual(['line 1', 'line 2'], comment.lines)
