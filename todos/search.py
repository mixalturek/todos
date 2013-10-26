#!/usr/bin/env python3
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
Searching of the comments.
"""


###############################################################################
####

import os
import re

from . import exceptions


###############################################################################
####

class Comment(object):
    """
    Container to store one comment that was found.
    """

    def __init__(self, str_pattern, path, position, lines):
        """
        Class constructor, initialize all members.
        """
        self.str_pattern = str_pattern
        # """ The pattern that was searched and found. """

        self.path = path
        # """ The input file. """

        self.position = position
        # """ The position in the file. """

        self.lines = lines
        # """ The matching line and optionally several lines after it. """


###############################################################################
####

class Pattern(object):
    """
    Container to store one pattern (regular expression) for searching.
    """


    def __init__(self, str_pattern, re_pattern):
        """
        Class constructor, initialize all members.
        """
        self.str_pattern = str_pattern
        # """ The string representation of the pattern. """

        self.re_pattern = re_pattern
        # """ The precompiled pattern. """


    def __str__(self):
        """
        Return a string representation of the pattern.
        """
        return self.str_pattern


###############################################################################
####

class Summary(object):
    """
    Container to store a summary of the comments searching.
    """

    def __init__(self, parameters):
        """
        Class constructor, initialize all members to zero or empty list.
        """
        self.total_files = 0
        # """ The number of the examined files. """

        self.total_directories = 0
        # """ The number of the examined directories. """

        self.per_pattern = {}
        # """ Summary per pattern. """

        self.per_file = {}
        # """ Summary per file. """

        for str_pattern in parameters.patterns:
            self.per_pattern[str_pattern] = 0


###############################################################################
####

class CommentsSearch(object):
    """
    Search comments in the source files.
    """

    def __init__(self, parameters, logger):
        """
        Class constructor, prepare the object for searching.
        """
        self.parameters = parameters
        # """ The input parameters. """

        self.logger = logger
        # """ The logger to output messages. """

        self.comments = []
        # """ The comments that was found during the searching. """

        self.summary = Summary(parameters)
        # """ The summary of the searching. """

        flags = 0
        if self.parameters.ignore_case:
            flags = re.IGNORECASE

        self.parameters.compiled_patterns = []
        for str_pattern in self.parameters.patterns:
            try:
                self.parameters.compiled_patterns.append(
                        Pattern(str_pattern, re.compile(str_pattern, flags))
                )
            except re.error as re_exception:
                raise exceptions.TodosFatalError(
                        'Pattern compilation failed: {0}, {1}'.
                        format(str_pattern, re_exception))


    def search(self):
        """
        Recursively search the comments according to the input parameters.
        """
        self.process_directories()


    def process_directories(self):
        """
        Process all directories.
        """
        for directory in self.parameters.directories:
            self.process_directory(directory, directory)


    def is_directory_suppressed(self, dir_name):
        """
        Return true if the input directory should be skipped, otherwise false.
        """
        if self.parameters.suppressed is None:
            return False

        return dir_name in self.parameters.suppressed


    def process_directory(self, directory, dir_name):
        '''
        Recursively search files in the input directory.
        '''
        if not os.path.isdir(directory):
            self.logger.verbose('Skipping directory (not a directory): {0}'.
                    format(directory))
            return

        if self.is_directory_suppressed(dir_name):
            self.logger.verbose('Skipping directory (suppressed): {0}'.
                    format(directory))
            return

        self.summary.total_directories += 1

        for item in os.listdir(directory):
            path = os.path.join(directory, item)

            if os.path.isfile(path):
                self.process_file(path)
            else:
                self.process_directory(path, item)


    def is_file_extension_allowed(self, path):
        """
        Return true if the input file should be processed, otherwise false.
        """
        if self.parameters.extensions is None:
            return True

        for extension in self.parameters.extensions:
            if path.endswith(extension):
                return True

        return False


    def is_file_binary(self, path):
        """
        Return true if the input file is considered as binary, otherwise false.
        Note the return value may be incorrect, only beginning of the file is
        examined for '\0' character.
        """
        const_chunk_size = 1024

        try:
            with open(path, 'rb') as input_file:
                chunk = input_file.read(const_chunk_size)
        except IOError as io_exception:
            self.logger.warn('Reading from file failed: {0}, {1}'.
                    format(path, io_exception))
            return True

        # If the beginning of the file contains a null byte, guess that the
        # file is binary. GNU grep works similarly, see file_is_binary()
        # in its source codes.
        #
        # The following works nicely for common ascii/utf8 encoded source codes
        # with binary object files, images and jar packages in the same
        # directory tree. The heuristic can be extended in future if needed,
        #
        # Note UTF-16 encoded text files will be clasified as binary,
        # is it correct/incorrect?
        # 0 means '\0' here
        return 0 in chunk


    def process_file(self, path):
        '''
        Process all lines of the input file.
        '''
        if not self.is_file_extension_allowed(path):
            self.logger.verbose('Skipping file (file extension): {0}'.
                    format(path))
            return

        if self.is_file_binary(path):
            self.logger.verbose('Skipping file (binary file): {0}'.format(path))
            return

        self.logger.verbose('Parsing file: {0}'.format(path))

        try:
            with open(path, mode='r', encoding=self.parameters.encoding) as input_file:
                lines = input_file.readlines()

            self.summary.total_files += 1
            self.summary.per_file[path] = 0

            position = 0
            for line in lines:
                position += 1
                self.process_line(path, position, line, lines)
        except IOError as io_exception:
            self.logger.warn('Reading from file failed: {0}, {1}'.
                    format(path, io_exception))
        except UnicodeError as unicode_exception:
            self.logger.warn('Skipping file (unicode error): {0}, {1}'.
                    format(path, unicode_exception))


    def contains_comment(self, line):
        """
        Return true if the input line contains a comment, otherwise false.
        """
        for comment in self.parameters.comments:
            if line.count(comment) > 0:
                return True

        return False


    def process_line(self, path, position, line, lines):
        '''
        Process the input line, search comment with one of the specified
        patterns.
        '''
        if not self.contains_comment(line):
            return

        for pattern in self.parameters.compiled_patterns:
            if pattern.re_pattern.search(line):
                lines_to_store = self.get_lines(lines, position-1,
                        self.parameters.num_lines)
                self.comments.append(Comment(pattern.str_pattern, path,
                        position, lines_to_store))
                self.summary.per_pattern[pattern.str_pattern] += 1
                self.summary.per_file[path] += 1
                break


    def get_lines(self, lines, position, count):
        '''
        Return content of the specified number of lines.
        '''
        last_line = position+count
        if last_line >= len(lines):
            last_line = len(lines)

        result = []
        for i in range(position, last_line):
            result.append(lines[i].rstrip())

        return result
