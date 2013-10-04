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

import ply.yacc
import tempfile
from elin.lexer import tokens


def p_exprs(p):
    ''' exprs :
              | expr exprs '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]


def p_expr(p):
    ''' expr : number
             | list
             | quote
             | identifier
             | string '''
    p[0] = p[1]


def p_number(p):
    ''' number : DIGITS '''
    p[0] = int(p[1])


def p_list(p):
    ''' list : LPAREN exprs RPAREN '''
    p[0] = p[2]


def p_quote(p):
    ''' quote : QUOTE expr '''
    p[0] = ["quote", p[2]]


def p_identifier(p):
    ''' identifier : IDENTIFIER '''
    p[0] = p[1]


def p_string(p):
    ''' string : STRING '''
    p[0] = p[1][1:-1].replace("\\\"", '"').encode("utf8")


def p_error(p):
    raise SyntaxError(p)


tmp = tempfile.gettempdir()
parser = ply.yacc.yacc(debug=False, outputdir=tmp)


def parse(text):
    global parser
    parser = ply.yacc.yacc(debug=False, outputdir=tmp)
    return parser.parse(text)
