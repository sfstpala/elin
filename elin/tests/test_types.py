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

import unittest
from elin.types import (
    List, Number, Symbol, String
)


class TypesTest(unittest.TestCase):

    def test_expression(self):
        pass

    def test_symbol(self):
        self.assertEqual(Symbol("test"), Symbol("test"))
        self.assertNotEqual(Symbol("test"), "test")
        self.assertNotEqual(Symbol("test"), String("test"))
        self.assertEqual(repr(Symbol("x")), "x")

    def test_list(self):
        self.assertEqual(List("test"), List("test"))
        self.assertNotEqual(List("test"), ["test"])
        self.assertNotEqual(List("test"), List("test", 1))
        self.assertIsInstance(List() + List(), List)
        self.assertEqual(List(1) < List(), [1] < [])
        self.assertEqual(repr(List(1)), "(1)")

    def test_string(self):
        self.assertEqual(repr(String("a\"b\n\r\v\t")), '"a\\"b\\n\\r\\v\\t"')
        self.assertIsInstance(String("a") + String("b"), String)

    def test_number(self):
        self.assertEqual(Number(0), Number(0))
        self.assertNotEqual(Number(0), Number(1))
        self.assertIsInstance(Number(1) + Number(1), Number)
        self.assertEqual(Number(2) + Number(2), Number(4))
        self.assertEqual(Number(2) - Number(2), Number(0))
        self.assertEqual(Number(2) * Number(2), Number(4))
        self.assertEqual(Number(10) / Number(3), Number(10.0 / 3.0))
        self.assertEqual(Number(10) // Number(3), Number(3))
        self.assertEqual(Number(10) % Number(3), Number(1))
        self.assertEqual(Number(3) ** Number(2), Number(9))
        for i in range(4):
            for j in range(4):
                self.assertEqual(Number(i) < Number(j), i < j)
                self.assertEqual(Number(i) <= Number(j), i <= j)
                self.assertEqual(Number(i) == Number(j), i == j)
                self.assertEqual(Number(i) != Number(j), i != j)
                self.assertEqual(Number(i) >= Number(j), i >= j)
                self.assertEqual(Number(i) > Number(j), i > j)
        self.assertEqual(repr(Number(100)), "100")
        self.assertEqual(repr(Number(1.4)), "1.4")
