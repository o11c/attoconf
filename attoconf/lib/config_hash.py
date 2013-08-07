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

from hashlib import md5
import os

from ..classy import ClassyProject


def calc_hash(build):
    hash = md5()
    for var, (val, origin), in sorted(build.vars.iteritems()):
        # origin is not included in the hash
        hash.update('%s = %s\n' % (var, val))
    return hash.hexdigest()


def add_config_hash(build):
    print('Generating a hash of config options ...')
    build.vars['CONFIG_HASH'] = (calc_hash(build), 'special')


class ConfigHash(ClassyProject):
    ''' Post hook add the build hash.

        This should be run before any other post hooks.
    '''
    __slots__ = ()

    def post(self):
        self.order.insert(0, 'CONFIG_HASH')
        self.checks.append(add_config_hash)
        super(ConfigHash, self).post()
