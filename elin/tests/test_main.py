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
import elin.__main__
import elin.lexer
import elin.interpreter
import elin.types

import unittest
import io
import sys


class MainTest(unittest.TestCase):

    def setUp(self):
        self.__stdio = sys.stdout, sys.stderr, sys.stdin
        sys.stdout, sys.stderr, sys.stdin = (io.StringIO() for i in range(3))

    def tearDown(self):
        sys.stdout, sys.stderr, sys.stdin = self.__stdio

    def test_help(self):
        self.assertRaises(SystemExit, elin.__main__.main, ["--help"])
        self.assertRegex(sys.stdout.getvalue(), r"^usage: elin")

    def test_version(self):
        self.assertRaises(SystemExit, elin.__main__.main, ["--version"])
        self.assertRegex(sys.stderr.getvalue(), r"^\d+\.\d+\.\d+$")

    def test_errno2(self):
        self.assertRaises(SystemExit, elin.__main__.main,
                          ["does-not-exist.txt"])
        self.assertRegex(sys.stderr.getvalue(),
                         r"\[Errno 2\] No such file or directory:")

    def test_run(self):
        self.assertRaises(SystemExit, elin.__main__.main, ["/dev/null"])
        self.assertEqual(sys.stderr.getvalue(), "")

    def test_unbalanced(self):
        self.assertTrue(elin.__main__.unbalanced(elin.lexer.lex("((")))

    def test_evaluate(self):
        interpreter = elin.interpreter.Interpreter()
        self.assertRaises(SystemExit, elin.__main__.evaluate, interpreter,
                          "))((", do_exit=True)
        self.assertRegex(sys.stderr.getvalue(), r"[eE]rror.+line \d+")
        self.assertIsInstance(elin.__main__.evaluate(
            interpreter, "12", do_exit=True), elin.types.Number)
        self.assertRaises(SystemExit, elin.__main__.evaluate, interpreter,
                          "(apply)", do_exit=True)
        self.assertRegex(sys.stderr.getvalue(), r"[eE]rror.+line \d+")

    def gen_test_interactive(self, code, expected):
        stdin, stdout, stderr = io.StringIO(code), sys.stdout, sys.stderr

        def input_fn(prompt):
            print(prompt, end="")
            sys.stdout.flush()
            i = stdin.readline()
            print(i)
            return i
        try:
            sys.stdout = sys.stderr = io.StringIO()
            res = elin.__main__.run(
                stdin, input_fn=input_fn,
                force_tty=True, once=True)
            output = sys.stdout.getvalue()
            self.assertIn(elin.__main__.WLC + "\n", output)
            output = output.replace(elin.__main__.WLC + "\n", "")
            self.assertEqual(output, expected)
        finally:
            sys.stdout, sys.stderr = stdout, stderr

    def test_interactive(self):
        self.gen_test_interactive(
            "((lambda (x) x)\n100)",
            "{}((lambda (x) x)\n\n"
            "{}100)\n"
            "= 100\n".format(elin.__main__.PS1, elin.__main__.PS2))

    def test_interactive_syntax_error(self):
        self.gen_test_interactive(
            "\"hello",
            "{}\"hello\n"
            "SyntaxError: line 1 (near '\"hello')\n".format(elin.__main__.PS1))
