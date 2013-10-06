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
from elin.lexer import lex


class TestLexer(unittest.TestCase):

    def test_lineno(self):
        one, two, three = tuple(lex("1\n2\n3\n"))
        self.assertEqual(one.lineno, 1)
        self.assertEqual(two.lineno, 2)
        self.assertEqual(three.lineno, 3)

    def test_LPAREN(self):
        t = tuple((i.type, i.value) for i in lex("((("))
        self.assertEqual(t, (
            ("LPAREN", "("), ("LPAREN", "("), ("LPAREN", "(")))

    def test_RPAREN(self):
        t = tuple((i.type, i.value) for i in lex(")))"))
        self.assertEqual(t, (
            ("RPAREN", ")"), ("RPAREN", ")"), ("RPAREN", ")")))

    def test_QUOTE(self):
        t = tuple((i.type, i.value) for i in lex("'''"))
        self.assertEqual(t, (
            ("QUOTE", "'"), ("QUOTE", "'"), ("QUOTE", "'")))

    def test_SEMICOLON(self):
        t = tuple((i.type, i.value) for i in lex(";;;"))
        self.assertEqual(t, ())

    def test_DIGITS(self):
        t = tuple((i.type, i.value) for i in lex('12'))
        self.assertEqual(t, (
            ("DIGITS", "12"), ))

    def test_IDENTIFIER(self):
        t = tuple((i.type, i.value) for i in lex('world*'))
        self.assertEqual(t, (
            ("IDENTIFIER", "world*"), ))

    def test_error(self):
        self.assertRaises(SyntaxError, lambda: tuple(lex("\"hello")))
