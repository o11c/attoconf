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

from attoconf.version import require_version, string as version_string

class TestVersion(unittest.TestCase):
    def test_parse(self):
        # don't do this
        name, version, dist = version_string.split(' ', 2)
        self.assertEqual(name, 'attoconf')
        major, minor, patch = [int(x) for x in version.split('.')]
        assert dist.startswith('(')
        assert dist.endswith(')')
        dist = dist[1:-1]
        assert '(' not in dist
        assert ')' not in dist
        assert '\n' not in dist
        from attoconf._version import distributor
        self.assertEqual(dist, distributor)

    def test_check(self):
        from attoconf._version import major, minor, patch
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor - 1, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor - 1, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor - 1, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 0, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 0, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 0, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 1, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 1, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major - 1, minor + 1, patch + 1)
        if 1:
            require_version(major + 0, minor - 1, patch - 1)
        if 1:
            require_version(major + 0, minor - 1, patch + 0)
        if 1:
            require_version(major + 0, minor - 1, patch + 1)
        if 1:
            require_version(major + 0, minor + 0, patch - 1)
        if 1:
            require_version(major + 0, minor + 0, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major + 0, minor + 0, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major + 0, minor + 1, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major + 0, minor + 1, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major + 0, minor + 1, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor - 1, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor - 1, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor - 1, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 0, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 0, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 0, patch + 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 1, patch - 1)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 1, patch + 0)
        with self.assertRaises(SystemExit):
            require_version(major + 1, minor + 1, patch + 1)
