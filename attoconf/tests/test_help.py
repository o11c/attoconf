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

from attoconf.help import Help, HelpSection, put_line_in_width

from cStringIO import StringIO

class TestHelpSection(unittest.TestCase):
    def test_basic(self):
        sec = HelpSection()
        sec.add_text('foo', False)
        sec.add_option('--foo', 'FOO', True)
        sec.add_text('bar', True)
        sec.add_option('--bar', 'BAR', False)
        self.assertEqual(sec.headers, [(False, 'foo'), (True, 'bar')])
        self.assertEqual(sec.options, [(True, '--foo', 'FOO'), (False, '--bar', 'BAR')])

        out = StringIO()
        sec.print(out, False, float('inf'))
        self.assertEqual(out.getvalue(), '''foo
  --bar  BAR
''')

        out = StringIO()
        sec.print(out, True, float('inf'))
        self.assertEqual(out.getvalue(), '''foo
bar
  --foo  FOO
  --bar  BAR
''')

    def test_width(self):
        out = StringIO()
        put_line_in_width(out, 'foo bar baz', float('inf'), 0)
        self.assertEqual(out.getvalue(), 'foo bar baz\n')

        out = StringIO()
        put_line_in_width(out, 'foo bar baz', 10, 0)
        self.assertEqual(out.getvalue(), 'foo bar\nbaz\n')

        out = StringIO()
        put_line_in_width(out, 'foo bar baz', 10, 2)
        self.assertEqual(out.getvalue(), 'foo bar\n  baz\n')

        out = StringIO()
        put_line_in_width(out, '   foo bar baz', 10, 0)
        self.assertEqual(out.getvalue(), '   foo bar\nbaz\n')

        out = StringIO()
        put_line_in_width(out, '    foo bar baz', 10, 0)
        self.assertEqual(out.getvalue(), '    foo\nbar baz\n')

        out = StringIO()
        put_line_in_width(out, '    foo bar baz', 10, 3)
        self.assertEqual(out.getvalue(), '    foo\n   bar baz\n')

        out = StringIO()
        put_line_in_width(out, '    foo bar baz', 10, 4)
        self.assertEqual(out.getvalue(), '    foo\n    bar\n    baz\n')

        out = StringIO()
        put_line_in_width(out, 'really-long-string', float('inf'), 0)
        self.assertEqual(out.getvalue(), 'really-long-string\n')

        out = StringIO()
        put_line_in_width(out, '  really-long-string', float('inf'), 0)
        self.assertEqual(out.getvalue(), '  really-long-string\n')

        out = StringIO()
        put_line_in_width(out, 'really-long-string', 10, 0)
        self.assertEqual(out.getvalue(), 'really-long-string\n')

        out = StringIO()
        put_line_in_width(out, '  really-long-string', 10, 0)
        self.assertEqual(out.getvalue(), '  really-long-string\n')

        out = StringIO()
        put_line_in_width(out, 'short really-long-string', float('inf'), 0)
        self.assertEqual(out.getvalue(), 'short really-long-string\n')

        out = StringIO()
        put_line_in_width(out, '  short really-long-string', float('inf'), 0)
        self.assertEqual(out.getvalue(), '  short really-long-string\n')

        out = StringIO()
        put_line_in_width(out, 'short really-long-string', 10, 0)
        self.assertEqual(out.getvalue(), 'short\nreally-long-string\n')

        out = StringIO()
        put_line_in_width(out, '  short really-long-string', 10, 0)
        self.assertEqual(out.getvalue(), '  short\nreally-long-string\n')

        out = StringIO()
        put_line_in_width(out, 'short really-long-string', 10, 1)
        self.assertEqual(out.getvalue(), 'short\n really-long-string\n')

        out = StringIO()
        put_line_in_width(out, '  short really-long-string', 10, 1)
        self.assertEqual(out.getvalue(), '  short\n really-long-string\n')

    def test_print(self):
        sec = HelpSection()
        sec.add_option('--abcdefghijklmnopqrstuvwxyz',
                'ABCDEFGHIJKLMNOPQRSTUVWXYZ', False)

        out = StringIO()
        sec.print(out, False, 80)
        self.assertEqual(out.getvalue(), '''
  --abcdefghijklmnopqrstuvwxyz
                    ABCDEFGHIJKLMNOPQRSTUVWXYZ
'''[1:])

        sec.add_option('--foo', 'FOO', False)
        sec.add_option('--frob', 'FROB', False)

        out = StringIO()
        sec.print(out, False, 80)
        self.assertEqual(out.getvalue(), '''
  --abcdefghijklmnopqrstuvwxyz
          ABCDEFGHIJKLMNOPQRSTUVWXYZ
  --foo   FOO
  --frob  FROB
'''[1:])

        out = StringIO()
        sec.print(out, False, float('inf'))
        self.assertEqual(out.getvalue(), '''
  --abcdefghijklmnopqrstuvwxyz  ABCDEFGHIJKLMNOPQRSTUVWXYZ
  --foo                         FOO
  --frob                        FROB
'''[1:])


class TestHelp(unittest.TestCase):
    def test_print(self):
        help = Help()
        help.add_option('--invisible', 'You can\'t see this', True)
        help.add_text('General:', False)
        help.add_option('--help', 'show this', False)
        help.add_option('--version', 'show that', True)
        help.add_text('Other stuff:', False)
        help.add_text('with long header:', True)
        help.add_option('--foo-lets-make-it-long-just-because', 'I\'m bored', False)
        help.add_text('Visibility:', False)
        help.add_option('--sneaky', 'This may be surprising. It also works as a demonstration of multi-line wrapping, just because.', True)

        out = StringIO()
        help.print(out, True, 80)
        self.assertEqual(out.getvalue(), '''
  --invisible  You can't see this

General:
  --help     show this
  --version  show that

Other stuff:
with long header:
  --foo-lets-make-it-long-just-because
                    I'm bored

Visibility:
  --sneaky  This may be surprising. It also works as a demonstration of
            multi-line wrapping, just because.

'''[1:])

        out = StringIO()
        help.print(out, False, 80)
        self.assertEqual(out.getvalue(), '''
General:
  --help  show this

Other stuff:
  --foo-lets-make-it-long-just-because
                    I'm bored

'''[1:])
