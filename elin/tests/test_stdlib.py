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
import sys
import io
from elin.stdlib import builtins
from elin.types import (
    List, Number, Symbol, String, Procedure
)


class StdlibTest(unittest.TestCase):

    def test_singletons(self):
        self.assertEqual(builtins[Symbol("#t")], Symbol("#t"))
        self.assertEqual(builtins[Symbol("#f")], Symbol("#f"))
        self.assertEqual(builtins[Symbol("nil")], List())

    def test_unary(self):
        self.assertEqual(builtins[Symbol("true?")](
            Number(10)), Symbol("#t"))
        self.assertEqual(builtins[Symbol("true?")](
            Number(10)), Symbol("#t"))
        self.assertEqual(builtins[Symbol("zero?")](
            Number(0)), Symbol("#t"))
        self.assertEqual(builtins[Symbol("zero?")](
            Symbol("#f")), Symbol("#f"))
        self.assertEqual(builtins[Symbol("not")](
            Number(10)), Symbol("#f"))
        self.assertEqual(builtins[Symbol("floor")](
            Number(0.5)), Number(0))
        self.assertEqual(builtins[Symbol("floor")](
            Number(-0.5)), Number(0))
        self.assertEqual(builtins[Symbol("abs")](
            Number(-0.5)), Number(0.5))
        self.assertEqual(builtins[Symbol("abs")](
            Number(0.5)), Number(0.5))

    def test_binary(self):
        for p in (0, 1, 2):
            for q in (0, 1, 2, 3):
                self.assertEqual(builtins[Symbol("+")](
                    Number(p), Number(q)), Number(p + q), (p, q))
                self.assertEqual(builtins[Symbol("-")](
                    Number(p), Number(q)), Number(p - q), (p, q))
                self.assertEqual(builtins[Symbol("*")](
                    Number(p), Number(q)), Number(p * q), (p, q))
                self.assertEqual(builtins[Symbol("**")](
                    Number(p), Number(q)), Number(p ** q), (p, q))

    def test_binary_division(self):
        for p in (0, 1, 2):
            for q in (1, 2, 3):
                self.assertEqual(builtins[Symbol("/")](
                    Number(p), Number(q)), Number(p / q), (p, q))
                self.assertEqual(builtins[Symbol("//")](
                    Number(p), Number(q)), Number(p // q), (p, q))
                self.assertEqual(builtins[Symbol("%")](
                    Number(p), Number(q)), Number(p % q), (p, q))

    def test_binary_boolean(self):
        for p in (0, 1, 2):
            for q in (0, 1, 2, 3):
                self.assertEqual(
                    builtins[Symbol("<")](
                        Number(p), Number(q)), Symbol("#t")
                    if p < q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol("<=")](
                        Number(p), Number(q)), Symbol("#t")
                    if p <= q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol("!=")](
                        Number(p), Number(q)), Symbol("#t")
                    if p != q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol("==")](
                        Number(p), Number(q)), Symbol("#t")
                    if p == q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol(">=")](
                        Number(p), Number(q)), Symbol("#t")
                    if p >= q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol(">")](
                        Number(p), Number(q)), Symbol("#t")
                    if p > q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol("and")](
                        Number(p), Number(q)), Symbol("#t")
                    if p and q else Symbol("#f"), (p, q))
                self.assertEqual(
                    builtins[Symbol("or")](
                        Number(p), Number(q)), Symbol("#t")
                    if p or q else Symbol("#f"), (p, q))

    def test_higher_order(self):
        self.assertEqual(
            builtins[Symbol("map")](
                Procedure(lambda x: x ** Number(2), List(Symbol("x"))),
                List(Number(3), Number(4))),
            List(Number(9), Number(16)))

    def test_print(self):
        stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            self.assertEqual(builtins[Symbol("print")](
                String("OK")), Symbol("#f"))
            self.assertEqual(sys.stdout.getvalue(), "\"OK\"\n")
        finally:
            sys.stdout = stdout

    def test_panic(self):
        stderr = sys.stderr
        sys.stderr = io.StringIO()
        try:
            self.assertRaises(SystemExit, builtins[Symbol("panic")],
                              String("boing"))
            self.assertEqual(sys.stderr.getvalue(), "\"boing\"\n")
        finally:
            sys.stderr = stderr

    def test_typecheck_symbol(self):
        self.assertTrue(builtins[Symbol("symbol?")](Symbol("")))
        self.assertFalse(builtins[Symbol("symbol?")](List()))
        self.assertFalse(builtins[Symbol("symbol?")](String("")))
        self.assertFalse(builtins[Symbol("symbol?")](Number(0)))
        self.assertFalse(builtins[Symbol("symbol?")](
            Procedure(lambda: None, List())))

    def test_typecheck_list(self):
        self.assertFalse(builtins[Symbol("list?")](Symbol("")))
        self.assertTrue(builtins[Symbol("list?")](List()))
        self.assertFalse(builtins[Symbol("list?")](String("")))
        self.assertFalse(builtins[Symbol("list?")](Number(0)))
        self.assertFalse(builtins[Symbol("list?")](
            Procedure(lambda: None, List())))

    def test_typecheck_string(self):
        self.assertFalse(builtins[Symbol("string?")](Symbol("")))
        self.assertFalse(builtins[Symbol("string?")](List()))
        self.assertTrue(builtins[Symbol("string?")](String("")))
        self.assertFalse(builtins[Symbol("string?")](Number(0)))
        self.assertFalse(builtins[Symbol("string?")](
            Procedure(lambda: None, List())))

    def test_typecheck_number(self):
        self.assertFalse(builtins[Symbol("number?")](Symbol("")))
        self.assertFalse(builtins[Symbol("number?")](List()))
        self.assertFalse(builtins[Symbol("number?")](String("")))
        self.assertTrue(builtins[Symbol("number?")](Number(0)))
        self.assertFalse(builtins[Symbol("number?")](
            Procedure(lambda: None, List())))

    def test_typecheck_procedure(self):
        self.assertFalse(builtins[Symbol("procedure?")](Symbol("")))
        self.assertFalse(builtins[Symbol("procedure?")](List()))
        self.assertFalse(builtins[Symbol("procedure?")](String("")))
        self.assertFalse(builtins[Symbol("procedure?")](Number(0)))
        self.assertTrue(builtins[Symbol("procedure?")](
            Procedure(lambda: None, List())))

    def test_car(self):
        self.assertRaises(IndexError, builtins[Symbol("car")], List())
        self.assertEqual(builtins[
            Symbol("car")](List(Number(0), Number(1))), Number(0))

    def test_cdr(self):
        self.assertEqual(builtins[
            Symbol("cdr")](List()), List())
        self.assertEqual(builtins[
            Symbol("cdr")](List(Number(0))), List())
        self.assertEqual(builtins[
            Symbol("cdr")](List(Number(0), Number(1))), List(Number(1)))
