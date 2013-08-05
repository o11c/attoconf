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

from attoconf.core import Project, Build

from cStringIO import StringIO
import sys

class ReplacingStdout(object):
    __slots__ = ('old', 'new')
    def __init__(self, new):
        self.old = None
        self.new = new
    def __enter__(self):
        self.old = sys.stdout
        sys.stdout = self.new
    def __exit__(self, type, value, traceback):
        sys.stdout = self.old
        del self.old

class TestProject(unittest.TestCase):
    def test_help(self):
        proj = Project('foo')
        proj.add_help('General:', False)
        proj.add_alias('--help', ['--help=default'],
                help='display standard help, then exit', hidden=False)
        proj.add_option('--help', init=None,
                type=proj.do_help, check=None,
                help='display some subset of help', hidden=False,
                help_var='TYPE')
        proj.help.add_option('--help=hidden',
                help='display help you should never ever ever care about',
                hidden=True)
        proj.add_option('--foo', init='asdf',
                type=str, check=None,
                help='set frob target', hidden=False)
        proj.add_option('--bar', init=None,
                type=str, check=None,
                help='set frob source', hidden=False,
                help_def='FOO')

        build = Build(proj, 'bar')

        out = StringIO()
        with ReplacingStdout(out):
            with self.assertRaises(SystemExit):
                build.apply_arg('--help')
        self.assertEqual(out.getvalue(), '''
General:
  --help       display standard help, then exit
  --help=TYPE  display some subset of help
  --foo=FOO    set frob target [asdf]
  --bar=BAR    set frob source [FOO]

'''[1:])

        out = StringIO()
        with ReplacingStdout(out):
            with self.assertRaises(SystemExit):
                build.apply_arg('--help=hidden')
        self.assertEqual(out.getvalue(), '''
General:
  --help         display standard help, then exit
  --help=TYPE    display some subset of help
  --help=hidden  display help you should never ever ever care about
  --foo=FOO      set frob target [asdf]
  --bar=BAR      set frob source [FOO]

'''[1:])

    def test_path(self):
        proj = Project('foo/')
        build = Build(proj, 'bar/')
        self.assertEquals(build.project.srcdir, 'foo')
        self.assertEquals(build.builddir, 'bar')
        self.assertEquals(build.relative_source(), '../foo')

    def test_configure(self):
        def check_foo(bld, foo):
            self.assertEqual(foo, 'B')
        def check_bar(bld, bar):
            self.assertEqual(bar, 1)
        def check_qux(bld, qux):
            self.assertEqual(qux, None)
        def check_var(bld, var):
            self.assertEqual(var, 'value')

        proj = Project('.')
        proj.add_alias('--alias', ['--foo=A', '--bar=1', '--foo=B'],
                help=None, hidden=False)
        proj.add_option('--foo', init=None,
                type=str, check=check_foo,
                help='help for string foo', hidden=False)
        proj.add_option('--bar', init=0,
                type=int, check=check_bar,
                help='help for int bar', hidden=False)
        proj.add_option('--qux', init=None,
                type=int, check=check_qux,
                help='help for int qux', hidden=False)
        proj.add_option('VAR', init='',
                type=str, check=check_var,
                help='help for string VAR', hidden=False)

        build = Build(proj, '.')
        build.configure(['--alias'],
                {
                    'VAR': 'value',
                    'QUX': 'a',
                    '--qux': 'b',
                })
        self.assertEqual(build.vars,
                {
                    'FOO': ('B', 'command-line'),
                    'BAR': (1, 'command-line'),
                    'QUX': (None, 'default'),
                    'VAR': ('value', 'environment'),
                })
