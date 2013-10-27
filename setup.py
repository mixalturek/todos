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
Setup script for TODOs.
"""

from distutils.core import setup
import todos.version

setup(
    name = "todos",
    packages = ["todos"],
    scripts=['todos.sh'],
    version = todos.version.TodosVersion.VERSION,
    description = "Search TODO, FIXME and similar comments in project files.",
    author = "Michal Turek",
    author_email = "mixalturek@users.sf.net",
    url = "http://todos.sourceforge.net/",
    download_url =
            "http://downloads.sourceforge.net/project/todos/{0}/todos-{0}.zip".
            format(todos.version.TodosVersion.VERSION),
    keywords = ["search", "TODO", "FIXME", "comment"],
    license = "GNU GPLv3",
    platforms = "OS Independent",
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Topic :: Utilities",
        "Topic :: Text Processing :: General",
        "Topic :: Software Development :: Quality Assurance",
        ],
    long_description = """\
TODOs is a small command-line utility to search TODO, FIXME and similar
comments in project files. It is licensed under the terms of GNU GPL 3 license,
it requires Python 3 interpreter for its execution and it is not platform
specific.
"""
)
