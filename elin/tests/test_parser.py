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


class TestParser(unittest.TestCase):

    def test_number(self):
        self.assertEqual(parse("1"), [1])
        self.assertEqual(parse("1234"), [1234])

    def test_exprs(self):
        self.assertEqual(parse("12 3"), [
            12,
            3])

    def test_sexpr(self):
        self.assertEqual(parse("(12 3) ()"), [
            [12, 3],
            []])

    def test_quote(self):
        self.assertEqual(parse("'(12\n3)"), [
            ['quote', [12, 3]]])

    def test_identifier(self):
        self.assertEqual(parse("hello world*"), [
            "hello",
            "world*"])

    def test_comment(self):
        self.assertEqual(parse("one ; 1 2\ntwo"), [
            "one",
            "two"])

    def test_string(self):
        self.assertEqual(parse('""'), [
            b""])
        self.assertEqual(parse('"\""'), [
            b"\""])
        self.assertEqual(parse('"\\"" one'), [
            b'"',
            "one"])
        self.assertEqual(parse(r'"hello world"'), [
            b"hello world"])
        self.assertEqual(parse(r'"hello \"world\""'), [
            b"hello \"world\""])

    def test_program(self):
        self.assertEqual(parse("""
        (def (f x)
         (* x x))
        (f 12)
        (print '"hello world")
        """), [
            ['def', ['f', 'x'],
             ['*', 'x', 'x']],
            ['f', 12],
            ['print', ['quote', b"hello world"]]])
