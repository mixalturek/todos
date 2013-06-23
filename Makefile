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


###############################################################################
#### Options, configuration

BUILD_DIR = build


###############################################################################
#### Default

.PHONY: all
all:


.PHONY: extra
extra: tests pylint doc lines sloccount


###############################################################################
#### Unit tests

.PHONY: tests
tests:
	mkdir -p $(BUILD_DIR)
	nosetests --with-xunit --xunit-file=build/nosetests.xml --all-modules --traverse-namespace --with-coverage --cover-package=todos --cover-inclusive

	# Debian contains too old python-coverage package
	# python -m coverage xml --include=todos*


###############################################################################
####

.PHONY: pylint
pylint:
	pylint -f parseable todos | tee build/pylint.out


###############################################################################
#### Number of lines

.PHONY: lines
lines:
	cat `find . -name '*.py'` | wc -l


.PHONY: sloccount
sloccount:
	mkdir -p $(BUILD_DIR)
	sloccount --duplicates --wide --details src > $(BUILD_DIR)/sloccount.sc


###############################################################################
#### Documentation

.PHONY: doc
doc:
	mkdir -p $(BUILD_DIR)/doc
	doxygen Doxyfile


###############################################################################
#### Update QtCreator project

.PHONY: qtcreator
qtcreator:
	find . -type f \
		| grep -v '^\./build' \
		| grep -v '^\./\.' \
		| grep -v '\.pyc$$' \
		| sort > todos.files


###############################################################################
#### Clean

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
	find . -name '*.pyc' -exec rm {} \;
	find . -name '.coverage' -exec rm {} \;
