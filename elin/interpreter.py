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

from elin.types import (
    List, Number, Symbol, String, Procedure
)


class Memory:

    def __init__(self):
        self.data = [{}]

    def enter_scope(self):
        self.data.append({})

    def leave_scope(self):
        self.data.pop(-1)

    def get(self, key):
        for scope in self.data[::-1]:
            if key in scope:
                return scope[key]
        raise KeyError(key)

    def set_local(self, key, value):
        self.data[-1][key] = value

    def set_outer(self, key, value):
        self.data[-2][key] = value


class Interpreter:

    def __init__(self):
        self.memory = Memory()

    def special_define(self, expr):
        if len(expr) == 3 and isinstance(expr[1], Symbol):
            result = self.evaluate(expr[2])
            self.memory.set_outer(expr[1], result)
            return result
        if len(expr) >= 2 and isinstance(expr[1], List) and all(
                isinstance(i, List) and len(i) == 2 for i in expr[1]):
            result = List()
            for k, v in expr[1]:
                result = self.evaluate(v)
                self.memory.set_outer(k, result)
            for e in expr[2:]:
                result = self.evaluate(e)
            return result
        if len(expr) >= 2 and isinstance(expr[1], List) and all(
                isinstance(i, Symbol) for i in expr[1]):
            name, argn, body = expr[1][0], List(*expr[1][1:]), expr[2:]
            expr = List(Symbol("define"), name, List(
                Symbol("lambda"), argn, *body))
            return self.special_define(expr)
        raise SyntaxError(expr)

    def special_lambda(self, expr):
        if len(expr) >= 2 and isinstance(expr[1], List) and all(
                isinstance(i, Symbol) for i in expr[1]):
            argn = expr[1]
            body = expr[2:]

            def procedure(*args):
                for k, v in zip(argn, args):
                    self.memory.set_local(k, v)
                r = List()
                for expr in body:
                    r = self.evaluate(expr)
                return r
            return Procedure(procedure, argn)
        raise SyntaxError(expr)

    def special_quote(self, expr):
        if len(expr) == 2:
            return expr[1]
        raise SyntaxError(expr)

    def special_eval(self, expr):
        result = List()
        for e in expr[1:]:
            result = self.evaluate(self.evaluate(e))
        return result

    def special_apply(self, expr):
        if len(expr) >= 2:
            fn, *args = (self.evaluate(e) for e in expr[1:])
            return fn(*args)
        raise SyntaxError(expr)

    def evaluate(self, expr):
        self.memory.enter_scope()
        if isinstance(expr, List):
            if expr and expr[0] == Symbol("lambda"):
                result = self.special_lambda(expr)
            elif expr and expr[0] == Symbol("define"):
                result = self.special_define(expr)
            elif expr and expr[0] == Symbol("quote"):
                result = self.special_quote(expr)
            elif expr and expr[0] == Symbol("eval"):
                result = self.special_eval(expr)
            elif expr and expr[0] == Symbol("apply"):
                result = self.special_apply(expr)
            else:
                result = self.special_apply(List(Symbol('apply'), *expr))
        elif isinstance(expr, Number):
            result = expr
        elif isinstance(expr, String):
            result = expr
        elif isinstance(expr, Symbol):
            result = self.lookup(expr)
        self.memory.leave_scope()
        return result

    def lookup(self, expr):
        return self.memory.get(expr)
