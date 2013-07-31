# Copyright (C) 2013 Stefano Palazzo <stefano.palazzo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

all: elin.egg-info/
elin.egg-info/:
	@python3 setup.py egg_info

test: all
	@python3 setup.py -q test
	@pep8 .

dist:
	@python3 setup.py sdist

deb: distclean
	@dpkg-buildpackage -rfakeroot -D -us -uc -S -tc
	@dpkg-buildpackage -rfakeroot -D -us -uc -b -tc
	@lintian -E --pedantic \
	    ../python3-elin_*.deb ../elin_*.dsc ../elin_*.changes

ifdef DEB_HOST_ARCH
DESTDIR ?= /
PREFIX ?= usr/
install:
	@python3 setup.py install --no-compile \
	    --prefix="$(PREFIX)" --root="$(DESTDIR)" --install-layout=deb
endif

clean:
ifndef DEB_HOST_ARCH
	@rm -rfv elin.egg-info/ build/ dist/
endif
	@find -depth -name "__pycache__" -type d -exec rm -rfv {} \;

ifndef DEB_HOST_ARCH
distclean: clean
	@rm -rfv ../elin_*.deb ../elin_*.dsc ../elin_*.changes \
	    ../elin_*.tar.gz ../elin_*.build ../python3-elin_*.deb
endif
