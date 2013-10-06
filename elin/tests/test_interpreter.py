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
from elin.interpreter import Interpreter
from elin.interpreter import Memory
from elin.parser import parse
from elin.types import (
    List, Number, Symbol, String, Procedure
)


class InterpreterTest(unittest.TestCase):

    def evaluate(self, code):
        i = Interpreter()
        for e in parse(code):
            i.evaluate(e)
        return i

    def test_apply(self):
        i = self.evaluate("(define (f x) x) (define x (f 12))")
        self.assertEqual(i.memory.data[-1][Symbol('x')], Number(12))
        i = self.evaluate("(define (f x) x) (define x (apply f \"ok\"))")
        self.assertEqual(i.memory.data[-1][Symbol('x')], String("ok"))
        self.assertRaises(SyntaxError, self.evaluate, "(apply)")

    def test_quote(self):
        i = self.evaluate("(define s 'x)")
        self.assertEqual(i.memory.data[-1][Symbol('s')], Symbol("x"))
        self.assertRaises(SyntaxError, self.evaluate, "(quote)")
        self.assertRaises(SyntaxError, self.evaluate, "(quote 1 2 3)")

    def test_eval(self):
        i = self.evaluate("(define s (eval '10))")
        self.assertEqual(i.memory.data[-1][Symbol('s')], Number(10))

    def test_define(self):
        i = self.evaluate("(define x 0)")
        self.assertEqual(i.memory.data, [{Symbol('x'): Number(0)}])
        i = self.evaluate("(define ((x 0) (y 1))) x y")
        self.assertEqual(i.memory.data, [{
            Symbol('x'): Number(0), Symbol('y'): Number(1)}])
        i = self.evaluate("(define ((x 0) (y 1))) (define z x)")
        self.assertEqual(i.memory.data, [{
            Symbol('x'): Number(0), Symbol('y'): Number(1),
            Symbol('z'): Number(0)}])
        i = self.evaluate("(define ((x 0) (y 1)) (define z x) z)")
        self.assertEqual(i.memory.data, [{
            Symbol('x'): Number(0), Symbol('y'): Number(1)}])
        self.assertRaises(SyntaxError, self.evaluate, "(define)")
        self.assertRaises(SyntaxError, self.evaluate, "(define f)")
        self.assertRaises(SyntaxError, self.evaluate, "(define (()) 1)")

    def test_define_lambda_form(self):
        f = self.evaluate(
            "(define (f x) x)").memory.data[-1][Symbol("f")]
        self.assertIsInstance(f, Procedure)
        self.assertEqual(f(0), 0)
        self.assertRaises(TypeError, f)
        self.assertRaises(TypeError, f, 1, 2)
        f = self.evaluate(
            "(define (f x) f)").memory.data[-1][Symbol("f")]
        self.assertEqual(f(0), f)
        f = self.evaluate(
            "(define (f))").memory.data[-1][Symbol("f")]
        self.assertEqual(f(), List())

    def test_lambda(self):
        f = self.evaluate(
            "(define f (lambda (x) x))").memory.data[-1][Symbol("f")]
        self.assertIsInstance(f, Procedure)
        self.assertEqual(f(0), 0)
        self.assertRaises(TypeError, f)
        self.assertRaises(TypeError, f, 1, 2)
        self.assertRaises(SyntaxError, self.evaluate, "(lambda)")
        self.assertRaises(SyntaxError, self.evaluate, "(lambda x x)")
        self.assertRaises(SyntaxError, self.evaluate, "(lambda 1)")

    def test_lambda_multiarg(self):
        f = self.evaluate(
            "(define f (lambda (x) 9 9 x))").memory.data[-1][Symbol("f")]
        self.assertEqual(f(0), 0)
        self.assertRaises(TypeError, f)
        self.assertRaises(TypeError, f, 1, 2)
        f = self.evaluate(
            "(define f (lambda (x)))").memory.data[-1][Symbol("f")]
        self.assertEqual(f(0), List())

    def test_recursion_scope(self):
        f = self.evaluate(
            "(define f (lambda () f))").memory.data[-1][Symbol("f")]
        self.assertEqual(f(), f)
        f = self.evaluate(
            "(define ((f (lambda () f))))").memory.data[-1][Symbol("f")]
        self.assertEqual(f(), f)


class MemoryTest(unittest.TestCase):

    def test_scopes(self):
        m = Memory()
        k, v = Symbol("k"), Symbol("v")
        self.assertRaises(KeyError, m.get, k)
        m.enter_scope()
        m.set_local(k, v)
        self.assertEqual(m.get(k), v)
        m.leave_scope()
        m.enter_scope()
        m.set_outer(k, v)
        self.assertEqual(m.get(k), v)
        m.leave_scope()
        self.assertEqual(m.get(k), v)
