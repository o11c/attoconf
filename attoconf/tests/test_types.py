#   Copyright 2013 Ben Longbons <b.r.longbons@gmail.com>
#
#   This file is part of attoconf.
#
#   attoconf is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   attoconf is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with attoconf.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function, division, absolute_import

import unittest

from attoconf.types import enum, ShellList

class TestEnum(unittest.TestCase):
    def test_stuff(self):
        foobar = enum('foo', 'bar')
        foobar('foo')
        foobar('bar')
        with self.assertRaisesRegexp(ValueError, "'baz' not in {foo, bar}"):
            foobar('baz')

class TestShell(unittest.TestCase):
    def test_str(self):
        sh0 = ShellList('\\ ')
        self.assertEqual("' '", str(sh0))
        self.assertEqual([' '], sh0.list)
        sh1 = ShellList(' foo ')
        self.assertEqual('foo', str(sh1))
        self.assertEqual(['foo'], sh1.list)
        sh2 = ShellList(' "foo bar " baz')
        self.assertEqual("'foo bar ' baz", str(sh2))
        self.assertEqual(['foo bar ', 'baz'], sh2.list)
        sh3 = ShellList(""" "foo\\ bar\\"" 'baz\\ qux' ''\\''' frob\\ it """)
        self.assertEqual("""'foo\\ bar"' 'baz\\ qux' ''"'"'' 'frob it'""", str(sh3))
        self.assertEqual(['foo\\ bar"', 'baz\\ qux', "'", 'frob it'], sh3.list)

    def test_list(self):
        sh1 = ShellList(['foo'])
        self.assertEqual('foo', str(sh1))
        sh2 = ShellList(['foo bar ', 'baz'])
        self.assertEqual("'foo bar ' baz", str(sh2))
        sh3 = ShellList(['foo\\ bar"', 'baz\\ qux', "'", 'frob it'])
        self.assertEqual('\'foo\\ bar"\' \'baz\\ qux\' \'\'"\'"\'\' \'frob it\'', str(sh3))

    def test_add(self):
        sh0 = ShellList('')
        self.assertEqual(str(sh0 + sh0), '')
        self.assertEqual((sh0 + sh0).list, [])
        sh1 = ShellList(['foo bar', 'baz'])
        self.assertEqual(str(sh0 + sh1), "'foo bar' baz")
        self.assertEqual((sh0 + sh1).list, sh1.list)
        self.assertEqual(str(sh1 + sh1), "'foo bar' baz 'foo bar' baz")
