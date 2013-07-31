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

import setuptools


setuptools.setup(
    name="elin",
    version="0.1.0",
    license="GPLv3",
    description="Dynamic dialect of Lisp",
    long_description=(
        "Elin is an interpreted, dyanmic dialect of Lisp"),
    platforms="Debian GNU/Linux",
    author="Stefano Palazzo",
    author_email="stefano.palazzo@gmail.com",
    url="https://github.com/sfstpala/elin/",
    packages=["elin"],
    test_suite="elin.tests",
    entry_points={
        "console_scripts": [
            "elin = elin.__main__:main",
        ],
    },
    data_files=[
        ("share/man/man1", ["debian/elin.1"]),
    ],
)
