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


###############################################################################
#### Variables

PROJECT = todos
SOURCES = $(wildcard $(PROJECT)/*.py)

PREFIX=/usr/local
BINDIR=$(PREFIX)/bin
MANDIR=$(PREFIX)/man
PYTHON=/usr/bin/env python


###############################################################################
#### Default

.PHONY: all
all: $(BUILD_DIR)/$(PROJECT) $(BUILD_DIR)/README.md $(BUILD_DIR)/README.txt $(BUILD_DIR)/$(PROJECT).1


.PHONY: extra
extra: tests pylint doc lines sloccount


###############################################################################
#### Application

$(BUILD_DIR)/$(PROJECT): $(SOURCES)
	mkdir -p $(BUILD_DIR)
	rm -f $(BUILD_DIR)/$(PROJECT)
	zip --quiet $(BUILD_DIR)/$(PROJECT) $(SOURCES)
	zip --quiet --junk-paths $(BUILD_DIR)/$(PROJECT) $(PROJECT)/__main__.py
	echo '#!$(PYTHON)' > $(BUILD_DIR)/$(PROJECT)
	cat $(BUILD_DIR)/$(PROJECT).zip >> $(BUILD_DIR)/$(PROJECT)
	rm $(BUILD_DIR)/$(PROJECT).zip
	chmod a+x $(BUILD_DIR)/$(PROJECT)


###############################################################################
#### Documentation

$(BUILD_DIR)/README.md: $(SOURCES) utils/README.md.in $(BUILD_DIR)/$(PROJECT)
	COLUMNS=69 $(BUILD_DIR)/$(PROJECT) --help | python3 utils/create_readme.py


$(BUILD_DIR)/README.txt: $(BUILD_DIR)/README.md
	pandoc -f markdown -t plain $(BUILD_DIR)/README.md -o $(BUILD_DIR)/README.txt


$(BUILD_DIR)/$(PROJECT).1: $(BUILD_DIR)/README.md
	pandoc -s -f markdown -t man $(BUILD_DIR)/README.md -o $(BUILD_DIR)/$(PROJECT).1


###############################################################################
#### Install

.PHONY: install
install: $(BUILD_DIR)/$(PROJECT) $(BUILD_DIR)/$(PROJECT).1
	install -d $(DESTDIR)$(BINDIR)
	install -m 755 $(BUILD_DIR)/$(PROJECT) $(DESTDIR)$(BINDIR)
	install -d $(DESTDIR)$(MANDIR)/man1
	install -m 644 $(BUILD_DIR)/$(PROJECT).1 $(DESTDIR)$(MANDIR)/man1


.PHONY: install
uninstall:
	rm -f $(DESTDIR)$(BINDIR)/$(PROJECT)
	rm -f $(DESTDIR)$(MANDIR)/man1/$(PROJECT).1


###############################################################################
#### Unit tests

.PHONY: tests
tests:
	mkdir -p $(BUILD_DIR)
	nosetests --verbose --with-xunit --xunit-file=build/nosetests.xml --all-modules --traverse-namespace --with-coverage --cover-package=todos --cover-inclusive --cover-erase --cover-branches --cover-html --cover-html-dir=build/coverage --cover-xml --cover-xml-file=build/coverage.xml


###############################################################################
#### Pylint

.PHONY: pylint
pylint:
	mkdir -p $(BUILD_DIR)
	@# W0511 - TODO/FIXME string in the code
	@# R0201 - Method could be a function
	@# R0903 - Too few public methods
	pylint -f parseable -d W0511,R0201,R0903 todos | tee build/pylint.out


###############################################################################
#### Number of lines

.PHONY: lines
lines:
	cat `find . -name '*.py'` | wc -l


.PHONY: sloccount
sloccount:
	mkdir -p $(BUILD_DIR)
	sloccount --duplicates --wide --details todos tests > $(BUILD_DIR)/sloccount.sc


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
