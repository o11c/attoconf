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
    sys.exit('Unsupported Python version: %s\nattoconf requires Python 2.7' % sys.version)

def require_version(major, minor, patch=0):
    ''' Check that this is the right version of attoconf, or die trying.
    '''
    if major != _version.major:
        # Once I release attoconf 1.0, I *probably* won't ever
        # do another major upgrade - that would be difficult to package.
        sys.exit(
'''
This configure script requires a different major version of attoconf.
Major version changes are rare, and software written against the one
version is likely to need changes to work with the other version.

Current version: %s
Minimum required version: %d.%d.%d
''' % (full_version, major, minor, patch))
    if minor > _version.minor:
        # In the interest of good style, it sometimes *should* be rewritten.
        sys.exit(
'''
This configure script requires a newer minor version of attoconf.
Minor version changes are common, and software written against the one
minor version will work with all later minor versions.

Current version: %s
Minimum required version: %d.%d.%d
''' % (full_version, major, minor, patch))
    if minor == _version.minor and patch > _version.patch:
        sys.exit(
'''
This configure script requires a newer patch version of attoconf.
Patch versions are usually not released unless there is a bug in a minor
version, but it is possible that someone is using experimental features.
If there is one, upgrade to the latest minor version instead.

Current version: %s
Minimum required version: %d.%d.%d
''' % (full_version, major, minor, patch))

part_version = '%d.%d.%d' % (_version.major, _version.minor, _version.patch)
full_version = 'attoconf %s (%s)' % (part_version, _version.distributor)
