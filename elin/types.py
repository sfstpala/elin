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

import functools


class Expression:

    pass


class Symbol(Expression):

    def __init__(self, value, lineno=0):
        self.value, self.lineno = value, lineno

    def __repr__(self):
        return self.value

    def __eq__(self, other):
        return isinstance(other, Symbol) and self.value == other.value


@functools.total_ordering
class List(Expression):

    def __init__(self, *values, lineno=0):
        self.value, self.lineno = list(values), lineno

    def __eq__(self, other):
        return type(other) is List and self.value == other.value

    def __le__(self, other):
        return type(other) is List and self.value <= other.value

    def __repr__(self):
        return "(" + " ".join(repr(i) for i in self.value) + ")"

    def __add__(self, other):
        return List(*(self.value + other.value), lineno=self.lineno)

    def __iter__(self):
        return (i for i in self.value)


class String(Expression):

    def __init__(self, value, lineno=0):
        self.value, self.lineno = value, lineno

    def __eq__(self, other):
        return type(other) is String and self.value == other.value

    def __repr__(self):
        s = self.value
        s = s.replace("\"", "\\\"")
        s = s.replace("\r", "\\r")
        s = s.replace("\n", "\\n")
        s = s.replace("\v", "\\v")
        s = s.replace("\t", "\\t")
        return '"' + s + '"'

    def __add__(self, other):
        return String(self.value + other.value, lineno=self.lineno)


@functools.total_ordering
class Number(Expression):

    def __init__(self, value, lineno=0):
        self.value, self.lineno = int(value), lineno

    def __eq__(self, other):
        return type(other) is Number and self.value == other.value

    def __le__(self, other):
        return type(other) is Number and self.value <= other.value

    def __repr__(self):
        return repr(self.value)

    def __add__(self, other):
        return Number(self.value + other.value, lineno=self.lineno)

    def __sub__(self, other):
        return Number(self.value - other.value, lineno=self.lineno)

    def __mul__(self, other):
        return Number(self.value * other.value, lineno=self.lineno)

    def __truediv__(self, other):
        return Number(self.value / other.value, lineno=self.lineno)

    def __floordiv__(self, other):
        return Number(self.value // other.value, lineno=self.lineno)

    def __mod__(self, other):
        return Number(self.value % other.value, lineno=self.lineno)

    def __pow__(self, other):
        return Number(self.value ** other.value, lineno=self.lineno)