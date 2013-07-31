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

import elin
import elin.__main__

import unittest
import io
import sys


class MainTest(unittest.TestCase):

    def setUp(self):
        self.__stdio = sys.stdout, sys.stderr, sys.stdin
        sys.stdout, sys.stderr, sys.stdin = (io.StringIO() for i in range(3))

    def tearDown(self):
        sys.stdout, sys.stderr, sys.stdin = self.__stdio

    def test_help(self):
        self.assertRaises(SystemExit, elin.__main__.main, ["--help"])
        self.assertRegex(sys.stdout.getvalue(), r"^usage: elin")

    def test_version(self):
        self.assertRaises(SystemExit, elin.__main__.main, ["--version"])
        self.assertRegex(sys.stderr.getvalue(), r"^\d+\.\d+\.\d+$")
