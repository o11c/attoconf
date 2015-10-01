#   Copyright 2015 Ben Longbons <b.r.longbons@gmail.com>
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

import os
import sys

from ..classy import ClassyProject
from ..types import enum, ShellList

from .c import do_exec, TestError, C, Cxx


yesno = enum('yes', 'no')

def run_pkg_config(build, *args):
    PKG_CONFIG = build.vars['PKG_CONFIG']
    status, output = do_exec(build, PKG_CONFIG + list(args))
    if status:
        raise TestError(output)
    return output.strip()

def check_pkg_config(build, PKG_CONFIG):
    version = run_pkg_config(build, '--version')
    print('Found pkg-config: %s' % version)

def package_check(build, package, **var):
    assert len(var) == 1
    _package, enabled = var.popitem()
    enabled = enabled == 'yes'
    modversion = run_pkg_config(build, '--modversion', package)
    print("Found dependency '%s': %s" % (package, modversion))
    cppflags = run_pkg_config(build, '--cflags-only-I', package)
    cflags = run_pkg_config(build, '--cflags-only-other', package)
    ldflags = run_pkg_config(build, '--libs-only-L', '--libs-only-other', package)
    libs = run_pkg_config(build, '--libs-only-l', package)

    build.vars['CPPFLAGS'] += cppflags
    if 'CFLAGS' in build.vars:
        build.vars['CFLAGS'] += cflags
    if 'CXXFLAGS' in build.vars:
        build.vars['CXXFLAGS'] += cflags
    build.vars['LDFLAGS'] += ldflags
    build.vars['LIBS'] += libs

class PkgConfig(ClassyProject):
    ''' Fill CFLAGS etc by pkg-config for dependencies.
    '''
    __slots__ = ()
    _merge_slots_ = ('required_packages', 'optional_packages')

    def __init__(self, required_packages, optional_packages, **kwargs):
        assert isinstance(self, (C, Cxx))
        super(PkgConfig, self).__init__(**kwargs)
        self.required_packages = required_packages
        self.optional_packages = optional_packages

    def vars(self):
        super(PkgConfig, self).vars()
        self.add_option('PKG_CONFIG', init=['pkg-config'],
                type=ShellList, check=check_pkg_config,
                help='Tool to find dependencies', hidden=False)

    def packages(self):
        super(PkgConfig, self).packages()
        for package in self.required_packages:
            self._pkg_config_add_package(package, True)
        for package in self.optional_packages:
            self._pkg_config_add_package(package, False)

    def _pkg_config_add_package(self, package, hidden):
        positive = '--with-' + package
        negative = '--without-' + package
        #check = package_required_check if hidden else package_optional_check
        check = lambda build, **kwargs: package_check(build, package, **kwargs)
        level = 'required' if hidden else 'optional'
        help = "Build with %s dependency '%s'" % (level, package)
        self.add_option(positive, type=yesno, hidden=hidden, init='yes', check=check, help=help)
        # TODO: instead reveal one of the aliases and hide the main
        # this requires messing with help slightly
        self.add_alias(positive, [positive + '=yes'], help=None, hidden=True)
        self.add_alias(negative, [positive + '=no'], help=None, hidden=True)
