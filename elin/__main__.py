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

import elin
import elin.parser
import sys
import os
import argparse


def evaluate(text, do_exit=True):
    try:
        ast = elin.parser.parse(text)
    except SyntaxError as e:
        lineno, value = e.args[0]
        print("syntax error in line {} (near {})".format(
            lineno, repr(value)), file=sys.stderr)
        if do_exit:
            sys.exit(1)
    else:
        for i in ast:
            print(i)  # TODO


def unbalanced(t):
    l = len(tuple(i for i in t if i.type == "LPAREN"))
    r = len(tuple(i for i in t if i.type == "RPAREN"))
    return l != r


def run(f, ps1=">>> ", ps2="... "):
    if os.isatty(sys.stdin.fileno()) and f is sys.stdin:
        try:
            import readline
        except ImportError:
            pass
        try:
            while True:
                text = input(ps1)
                t = tuple(elin.lexer.lex(text))
                while unbalanced(t):
                    text += "\n" + input(ps2)
                    t = tuple(elin.lexer.lex(text))
                evaluate(text, do_exit=False)
        except (EOFError, KeyboardInterrupt):
            print(file=sys.stderr)
            sys.exit(0)
    else:
        evaluate(f.read())


def parse_args(args):
    parser = argparse.ArgumentParser(__package__)
    parser.add_argument(
        "--version", action="version", version=elin.__version__)
    parser.add_argument("file", nargs="?", type=open)
    try:
        return parser.parse_args(args)
    except IOError as e:
        print(e, file=sys.stderr)
        sys.exit(2)


def main(args=None):
    args = args if args is not None else sys.argv[1:]
    args = parse_args(args)
    try:
        run(args.file or sys.stdin)
    finally:
        if args.file is not None:
            args.file.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
