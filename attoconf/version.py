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

import sys

from . import _version

if sys.version_info[0] != 2 or sys.version_info[1] < 7:
    sys.exit('Unsupported Python version: %s\nRequire Python 2.7' % sys.version)

def require_version(major, minor, patch=0):
    ''' Check that this is the right version of attoconf, or die trying.
    '''

    actual = 'Current version: ' + string
    if major != _version.major:
        sys.exit('Unsupported major version: %d\n' % major + actual)
    if minor > _version.minor:
        sys.exit('Unsupported minor version: %d.%d\n' % (major, minor) + actual)
    if minor == _version.minor and patch > _version.patch:
        sys.exit('Unsupported patch version: %d.%d.%d\n' % (major, minor, patch) + actual)

string = 'attoconf %d.%d.%d (%s)' % (_version.major, _version.minor, _version.patch, _version.distributor)
