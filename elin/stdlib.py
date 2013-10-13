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

import sys
from elin.types import (
    List, Number, Symbol, String, Procedure
)


def bool_fn(b):
    return Symbol("#t") if b else Symbol("#f")


builtins = dict(
    tuple(({Symbol(k): v for k, v in ({
        "#t": Symbol("#t"),
        "#f": Symbol("#f"),
        "nil": List(),
    }).items()}).items()) +
    tuple(({Symbol(k): Procedure(v, List(
        Symbol("x"))) for k, v in ({
            "print": lambda x: print(x) or Symbol("#f"),
            "panic": lambda x: print(x, file=sys.stderr) or sys.exit(1),
            "true?": lambda x: bool_fn(x),
            "zero?": lambda x: bool_fn(x == Number(0)),
            "not": lambda x: bool_fn(not x),
            "floor": lambda x: x.floor(),
            "abs": lambda x: abs(x),
            "symbol?": lambda x: isinstance(x, Symbol),
            "list?": lambda x: isinstance(x, List),
            "string?": lambda x: isinstance(x, String),
            "number?": lambda x: isinstance(x, Number),
            "procedure?": lambda x: isinstance(x, Procedure),
            "car": lambda x: x[0],
            "cdr": lambda x: List(*x[1:]),
        }).items()}).items()) +
    tuple(({Symbol(k): Procedure(v, List(
        Symbol("x"), Symbol("y"))) for k, v in ({
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            "//": lambda x, y: x // y,
            "%": lambda x, y: x % y,
            "**": lambda x, y: x ** y,
            "<": lambda x, y: bool_fn(x < y),
            "<=": lambda x, y: bool_fn(x <= y),
            "!=": lambda x, y: bool_fn(x != y),
            "==": lambda x, y: bool_fn(x == y),
            ">=": lambda x, y: bool_fn(x >= y),
            ">": lambda x, y: bool_fn(x > y),
            "and": lambda x, y: bool_fn(x and y),
            "or": lambda x, y: bool_fn(x or y),
        }).items()}).items()) +
    tuple(({Symbol(k): Procedure(v, List(
        Symbol("fn"), Symbol("xs"))) for k, v in ({
            "map": lambda fn, xs: List(*map(fn, xs)),
        }).items()}).items()))
