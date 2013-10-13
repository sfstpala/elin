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
import elin.interpreter
import sys
import io
import os
import argparse
try:
    import readline
except ImportError:  # pragma: no cover
    pass


def evaluate(interpreter, text, do_exit=True):
    try:
        ast = elin.parser.parse(text)
    except SyntaxError as e:
        lineno, value = e.args[0]
        print("SyntaxError: line {} (near {})".format(
            lineno, repr(value)), file=sys.stderr)
        if do_exit:
            sys.exit(1)
    else:
        try:
            result = None
            for i in ast:
                result = interpreter.evaluate(i)
        except Exception as e:
            print(type(e).__name__, e, sep=": ", file=sys.stderr)
            if do_exit:
                sys.exit(1)
        return result


def unbalanced(t):
    l = len(tuple(i for i in t if i.type == "LPAREN"))
    r = len(tuple(i for i in t if i.type == "RPAREN"))
    return l != r


PS1 = "> "
PS2 = ".  "
WLC = "\n".join((
    "Welcome to Elin, a ridiculous Scheme dialect. Elin is free software",
    "under the terms of the GPL (v3). See '/usr/share/doc/elin/copyright'.",
    "The Elin reference manual is avaible at '/usr/share/doc/elin/ref.md'.",
))


def run(f, input_fn=input, force_tty=False, once=False):
    interpreter = elin.interpreter.Interpreter()
    try:
        tty = os.isatty(sys.stdin.fileno())
    except io.UnsupportedOperation:
        tty = False
    if force_tty or (tty and f is sys.stdin):
        print(WLC)
        try:
            while True:
                text = input_fn(PS1)
                try:
                    t = tuple(elin.lexer.lex(text))
                    while unbalanced(t):
                        text += "\n" + input_fn(PS2)
                        t = tuple(elin.lexer.lex(text))
                    result = evaluate(interpreter, text, do_exit=False)
                    if result is not None:
                        print("=", result)
                except SyntaxError as e:
                    lineno, value = e.args[0]
                    print("SyntaxError: line {} (near {})".format(
                        lineno, repr(value)), file=sys.stderr)
                if once:
                    break
        except (EOFError, KeyboardInterrupt):  # pragma: no cover
            print(file=sys.stderr)
            sys.exit(0)
    else:
        evaluate(interpreter, f.read())


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


if __name__ == '__main__':  # pragma: no cover
    main()
