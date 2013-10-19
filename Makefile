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


###############################################################################
#### Options, configuration

BUILD_DIR = build
DIST_DIR = dist


###############################################################################
#### Variables

PROJECT = todos
SOURCES = $(wildcard $(PROJECT)/*.py)

PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
MANDIR=$(PREFIX)/man
PYTHON=/usr/bin/env python3


###############################################################################
#### Default

.PHONY: all
all: $(BUILD_DIR)/README.md $(BUILD_DIR)/README.txt $(BUILD_DIR)/$(PROJECT).1 README dist


.PHONY: extra
extra: tests pylint doc lines sloccount


###############################################################################
#### Documentation

$(BUILD_DIR)/README.md: $(SOURCES) utils/README.md.in
	mkdir -p $(BUILD_DIR)
	COLUMNS=69 $(PYTHON) -m $(PROJECT) --help | $(PYTHON) utils/create_readme.py


$(BUILD_DIR)/README.txt: $(BUILD_DIR)/README.md
	pandoc -f markdown -t plain $(BUILD_DIR)/README.md -o $(BUILD_DIR)/README.txt


$(BUILD_DIR)/$(PROJECT).1: $(BUILD_DIR)/README.md
	pandoc -s -f markdown -t man $(BUILD_DIR)/README.md -o $(BUILD_DIR)/$(PROJECT).1

README: $(BUILD_DIR)/README.txt
	cp $(BUILD_DIR)/README.txt README


###############################################################################
#### Distribution packages

.PHONY: dist
dist:
	$(PYTHON) setup.py sdist
	# $(PYTHON) setup.py bdist_wininst
	# $(PYTHON) setup.py bdist_rpm


###############################################################################
#### Install

.PHONY: install
install: $(BUILD_DIR)/$(PROJECT).1
	# $(PYTHON) setup.py install
	install -d $(DESTDIR)$(MANDIR)/man1
	install -m 644 $(BUILD_DIR)/$(PROJECT).1 $(DESTDIR)$(MANDIR)/man1


.PHONY: uninstall
uninstall:
	# Python files installed using setup.py should be removed manually
	rm -f $(DESTDIR)$(BINDIR)/$(PROJECT)
	rm -f $(DESTDIR)$(MANDIR)/man1/$(PROJECT).1


###############################################################################
#### Unit tests

.PHONY: tests
tests:
	mkdir -p $(BUILD_DIR)
	# TODO: Use nosetests3 tool after it is available in Debian with coverage
	nosetests --verbose --with-xunit --xunit-file=build/nosetests.xml --all-modules --traverse-namespace --with-coverage --cover-package=$(PROJECT) --cover-inclusive --cover-erase --cover-branches --cover-html --cover-html-dir=build/coverage --cover-xml --cover-xml-file=build/coverage.xml


###############################################################################
#### Pylint

.PHONY: pylint
pylint:
	mkdir -p $(BUILD_DIR)
	@# W0511 - TODO/FIXME string in the code
	@# R0201 - Method could be a function
	@# R0903 - Too few public methods
	pylint -f parseable -d W0511,R0201,R0903 $(PROJECT) | tee build/pylint.out


###############################################################################
#### Number of lines

.PHONY: lines
lines:
	cat `find . -name '*.py'` | wc -l


.PHONY: sloccount
sloccount:
	mkdir -p $(BUILD_DIR)
	sloccount --duplicates --wide --details $(PROJECT) tests > $(BUILD_DIR)/sloccount.sc


###############################################################################
#### Doxygen

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
		| sort > $(PROJECT).files


###############################################################################
#### Clean

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR)
	rm -f MANIFEST
	rm -rf todos/__pycache__
	find . -name '*.pyc' -exec rm {} \;
	find . -name '.coverage' -exec rm {} \;
