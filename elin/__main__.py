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
import sys
import argparse


def parse_args(args):
    parser = argparse.ArgumentParser(__package__)
    parser.add_argument(
        "--version", action="version", version=elin.__version__)
    return parser.parse_args(args)


def main(args=None):
    args = args if args is not None else sys.argv[1:]
    args = parse_args(args)
    sys.exit(0)


if __name__ == '__main__':
    main()
