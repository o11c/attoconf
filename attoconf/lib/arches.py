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

from ..classy import ClassyProject
from ..types import triple

def host(build, HOST):
    if HOST is None:
        BUILD, origin = build.vars['BUILD']
        if origin != 'default':
            origin = 'derived from BUILD'
        build.vars['HOST'] = (BUILD, origin)

def target(build, TARGET):
    if TARGET is None:
        HOST, origin = build.vars['HOST']
        if origin != 'default':
            origin = 'derived from HOST'
        build.vars['TARGET'] = (HOST, origin)

class Arches2(ClassyProject):
    __slots__ = ()

    def arches(self):
        super(Arches2, self).arches()
        self.add_help('System types:', hidden=False)
        self.add_option('--build', init=None,
                type=triple, check=None,
                help='configure for building on BUILD', hidden=False,
                help_def='native')
        self.add_option('--host', init=None,
                type=triple, check=host,
                help='cross-compile to build programs to run on HOST',
                hidden=False, help_def='BUILD')

# TODO figure out the mro implications when I use this
class Arches3(Arches2):
    __slots__ = ()
    def arches(self):
        super(Arches3, self).arches()
        self.add_option('--target', init=None,
                type=triple, check=target,
                help='configure for building compilers for TARGET',
                hidden=False, help_def='HOST')
