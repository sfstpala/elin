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
from elin.parser import parse
from elin.types import (
    List, Number, Symbol, String
)


class TestParser(unittest.TestCase):

    def test_number(self):
        self.assertEqual(parse("1"), List(Number(1)))
        self.assertEqual(parse("1234"), List(Number(1234)))
        self.assertEqual(parse("-1"), List(Number(-1)))
        self.assertEqual(parse("1.0"), List(Number(1.0)))
        self.assertEqual(parse("-1.0"), List(Number(-1.0)))

    def test_exprs(self):
        self.assertEqual(parse("12 3"), List(
            Number(12),
            Number(3)))

    def test_sexpr(self):
        self.assertEqual(parse("(12 3) ()"), List(
            List(Number(12), Number(3)),
            List()))

    def test_quote(self):
        self.assertEqual(parse("'(12\n3)"), List(
            List(Symbol('quote'), List(Number(12), Number(3)))))

    def test_identifier(self):
        self.assertEqual(parse("hello world*"), List(
            Symbol("hello"),
            Symbol("world*")))

    def test_comment(self):
        self.assertEqual(parse("one ; 1 2\ntwo"), List(
            Symbol("one"),
            Symbol("two")))

    def test_string(self):
        self.assertEqual(parse('""'), List(
            String("")))
        self.assertEqual(parse(r'"\""'), List(
            String("\"")))
        self.assertEqual(parse('"\\"" one'), List(
            String('"'),
            Symbol("one")))
        self.assertEqual(parse(r'"hello world"'), List(
            String("hello world")))
        self.assertEqual(parse(r'"hello \"world\""'), List(
            String("hello \"world\"")))
        self.assertEqual(parse(r'"hello" "world"'), List(
            String("hello"), String("world")))

    def test_program(self):
        self.assertEqual(parse("""
        (def (f x)
         (* x x))
        (f 12)
        (print '"hello world")
        """), List(
            List(Symbol('def'), List(Symbol('f'), Symbol('x')),
                 List(Symbol('*'), Symbol('x'), Symbol('x'))),
            List(Symbol('f'), Number(12)),
            List(Symbol('print'),
                 List(Symbol('quote'), String("hello world")))))

    def test_error(self):
        self.assertRaises(SyntaxError, parse, "(((")
