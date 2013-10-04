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

import ply.lex

tokens = (
    "LPAREN",
    "RPAREN",
    "QUOTE",
    "STRING",
    "IDENTIFIER",
    "DIGITS",
)


t_LPAREN = "\\("
t_RPAREN = "\\)"
t_QUOTE = "'"
t_STRING = '\"(\\\"|[^\\]?[^\"])*\"'
t_IDENTIFIER = "[^()';\"\\\\\r\n\v\t\d ]+"
t_DIGITS = r"\d+"
t_ignore = "\r\v\t "


def t_comment(t):
    r';.*'
    pass


def t_newline(t):
    r'\n+'
    t.lexer.lineno += 1


def t_error(t):
    raise SyntaxError(
        (t.lexer.lineno, t.value[:30] +
         ("..." if len(t.value) > 31 else "")))


lexer = ply.lex.lex()


def lex(text):
    global lexer
    lexer = ply.lex.lex()
    lexer.input(text)
    while True:
        token = lexer.token()
        if not token:
            break
        yield token
