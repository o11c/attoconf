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

import os

from ..classy import ClassyProject
from ..types import shell_word, version, filepath, quoted_string


def exec_prefix(build, EPREFIX):
    if EPREFIX is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['EPREFIX'] = (PREFIX, origin)

def bindir(build, DIR):
    if DIR is None:
        EPREFIX, origin = build.vars['EPREFIX']
        if origin != 'default':
            origin = 'derived from EPREFIX'
        build.vars['BINDIR'] = (os.path.join(EPREFIX, 'bin'), origin)

def sbindir(build, DIR):
    if DIR is None:
        EPREFIX, origin = build.vars['EPREFIX']
        if origin != 'default':
            origin = 'derived from EPREFIX'
        build.vars['SBINDIR'] = (os.path.join(EPREFIX, 'sbin'), origin)

def libexecdir(build, DIR):
    if DIR is None:
        EPREFIX, origin = build.vars['EPREFIX']
        if origin != 'default':
            origin = 'derived from EPREFIX'
        build.vars['LIBEXECDIR'] = (os.path.join(EPREFIX, 'libexec'), origin)

def sysconfdir(build, DIR):
    if DIR is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['SYSCONFDIR'] = (os.path.join(PREFIX, 'etc'), origin)

def sharedstatedir(build, DIR):
    if DIR is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['SHAREDSTATEDIR'] = (os.path.join(PREFIX, 'com'), origin)

def localstatedir(build, DIR):
    if DIR is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['LOCALSTATEDIR'] = (os.path.join(PREFIX, 'var'), origin)

def libdir(build, DIR):
    if DIR is None:
        EPREFIX, origin = build.vars['EPREFIX']
        if origin != 'default':
            origin = 'derived from EPREFIX'
        build.vars['LIBDIR'] = (os.path.join(EPREFIX, 'lib'), origin)

def includedir(build, DIR):
    if DIR is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['INCLUDEDIR'] = (os.path.join(PREFIX, 'include'), origin)

def datarootdir(build, DIR):
    if DIR is None:
        PREFIX, origin = build.vars['PREFIX']
        if origin != 'default':
            origin = 'derived from PREFIX'
        build.vars['DATAROOTDIR'] = (os.path.join(PREFIX, 'share'), origin)

def datadir(build, DIR):
    if DIR is None:
        DATAROOTDIR, origin = build.vars['DATAROOTDIR']
        if origin != 'default':
            origin = 'derived from DATAROOTDIR'
        build.vars['DATADIR'] = (DATAROOTDIR, origin)

def packagedatadir(build, DIR):
    if DIR is None:
        DATADIR, origin = build.vars['DATADIR']
        PACKAGE, prigin = build.vars['PACKAGE']
        if origin != 'default' or prigin != 'default':
            origin = 'derived from DATADIR and PACKAGE'
        build.vars['DATADIR'] = (os.path.join(DATADIR, PACKAGE), origin)

def infodir(build, DIR):
    if DIR is None:
        DATAROOTDIR, origin = build.vars['DATAROOTDIR']
        if origin != 'default':
            origin = 'derived from DATAROOTDIR'
        build.vars['INFODIR'] = (os.path.join(DATAROOTDIR, 'info'), origin)

def localedir(build, DIR):
    if DIR is None:
        DATAROOTDIR, origin = build.vars['DATAROOTDIR']
        if origin != 'default':
            origin = 'derived from DATAROOTDIR'
        build.vars['LOCALEDIR'] = (os.path.join(DATAROOTDIR, 'locale'), origin)

def mandir(build, DIR):
    if DIR is None:
        DATAROOTDIR, origin = build.vars['DATAROOTDIR']
        if origin != 'default':
            origin = 'derived from DATAROOTDIR'
        build.vars['MANDIR'] = (os.path.join(DATAROOTDIR, 'man'), origin)

def docdir(build, DIR):
    if DIR is None:
        DATAROOTDIR, origin = build.vars['DATAROOTDIR']
        PACKAGE, origin2 = build.vars['PACKAGE']
        if origin != 'default' or origin2 != 'default':
            origin = 'derived from DATAROOTDIR and PACKAGE'
        build.vars['DOCDIR'] = (os.path.join(DATAROOTDIR, 'doc', PACKAGE), origin)

def htmldir(build, DIR):
    if DIR is None:
        DOCDIR, origin = build.vars['DOCDIR']
        if origin != 'default':
            origin = 'derived from DOCDIR'
        build.vars['HTMLDIR'] = (DOCDIR, origin)

def dvidir(build, DIR):
    if DIR is None:
        DOCDIR, origin = build.vars['DOCDIR']
        if origin != 'default':
            origin = 'derived from DOCDIR'
        build.vars['DVIDIR'] = (DOCDIR, origin)

def pdfdir(build, DIR):
    if DIR is None:
        DOCDIR, origin = build.vars['DOCDIR']
        if origin != 'default':
            origin = 'derived from DOCDIR'
        build.vars['PDFDIR'] = (DOCDIR, origin)

def psdir(build, DIR):
    if DIR is None:
        DOCDIR, origin = build.vars['DOCDIR']
        if origin != 'default':
            origin = 'derived from DOCDIR'
        build.vars['PSDIR'] = (DOCDIR, origin)


class Install(ClassyProject):
    __slots__ = ()

    @classmethod
    def slots(cls):
        return super(Install, cls).slots() + (
                'package', 'package_version', 'package_name')

    def set_package(self, package, version, name):
        self.package = package
        self.package_version = version
        self.package_name = name

    def general(self):
        super(Install, self).general()
        self.add_option('--package', init=self.package,
                type=shell_word, check=None,
                help='Short name of this package (don\'t change!)',
                hidden=True)
        self.add_option('--package-version', init=self.package_version,
                type=version, check=None,
                help='Version of this package (change in configure)',
                hidden=True,
                help_var='VERSION')
        self.add_option('--package-name', init=self.package_name,
                type=quoted_string, check=None,
                help='Long name of this package (don\'t change)',
                hidden=True,
                help_var='NAME')

    def paths(self):
        super(Install, self).paths()

        self.add_help('Installation directories:', hidden=False)
        self.add_option('--prefix', init='/usr/local',
                type=filepath, check=None,
                help='install architecture-independent files in PREFIX',
                hidden=False)
        self.add_option('--exec-prefix', init=None,
                type=filepath, check=exec_prefix,
                help='install architecture-dependent files in EPREFIX',
                hidden=False,
                var='EPREFIX', help_def='PREFIX')

        self.add_help('Fine tuning of the installation directories:',
                hidden=False)
        self.add_option('--bindir', init=None,
                type=filepath, check=bindir,
                help='user executables', hidden=False,
                help_var='DIR', help_def='EPREFIX/bin')
        self.add_option('--sbindir', init=None,
                type=filepath, check=sbindir,
                help='system admin executables', hidden=False,
                help_var='DIR', help_def='EPREFIX/sbin')
        self.add_option('--libexecdir', init=None,
                type=filepath, check=libexecdir,
                help='program executables', hidden=False,
                help_var='DIR', help_def='EPREFIX/libexec')
        self.add_option('--sysconfdir', init=None,
                type=filepath, check=sysconfdir,
                help='read-only single-machine data', hidden=False,
                help_var='DIR', help_def='PREFIX/etc')
        self.add_option('--sharedstatedir', init=None,
                type=filepath, check=sharedstatedir,
                help='modifiable architecture-independent data', hidden=False,
                help_var='DIR', help_def='PREFIX/com')
        self.add_option('--localstatedir', init=None,
                type=filepath, check=localstatedir,
                help='modifiable single-machine data', hidden=False,
                help_var='DIR', help_def='PREFIX/var')
        self.add_option('--libdir', init=None,
                type=filepath, check=libdir,
                help='object code libraries', hidden=False,
                help_var='DIR', help_def='EPREFIX/lib')
        self.add_option('--includedir', init=None,
                type=filepath, check=includedir,
                help='C header files', hidden=False,
                help_var='DIR', help_def='PREFIX/include')
        self.add_option('--oldincludedir', init='/usr/include',
                type=filepath, check=None,
                help='C header files for non-gcc', hidden=False,
                help_var='DIR')
        self.add_option('--datarootdir', init=None,
                type=filepath, check=datarootdir,
                help='read-only arch.-independent data root', hidden=False,
                help_var='DIR', help_def='PREFIX/share')
        self.add_option('--datadir', init=None,
                type=filepath, check=datadir,
                help='read-only architecture-independent data', hidden=False,
                help_var='DIR', help_def='DATAROOTDIR')
        self.add_option('--packagedatadir', init=None,
                type=filepath, check=packagedatadir,
                help='data specific to this package (please set datadir instead)', hidden=False,
                help_var='DIR', help_def='DATADIR/PACKAGE')
        self.add_option('--infodir', init=None,
                type=filepath, check=infodir,
                help='info documentation', hidden=False,
                help_var='DIR', help_def='DATAROOTDIR/info')
        self.add_option('--localedir', init=None,
                type=filepath, check=localedir,
                help='locale-dependent data', hidden=False,
                help_var='DIR', help_def='DATAROOTDIR/locale')
        self.add_option('--mandir', init=None,
                type=filepath, check=mandir,
                help='man documentation', hidden=False,
                help_var='DIR', help_def='DATAROOTDIR/man')
        self.add_option('--docdir', init=None,
                type=filepath, check=docdir,
                help='documentation root', hidden=False,
                help_var='DIR', help_def='DATAROOTDIR/doc/PACKAGE')
        self.add_option('--htmldir', init=None,
                type=filepath, check=htmldir,
                help='html documentation', hidden=False,
                help_var='DIR', help_def='DOCDIR')
        self.add_option('--dvidir', init=None,
                type=filepath, check=dvidir,
                help='dvi documentation', hidden=False,
                help_var='DIR', help_def='DOCDIR')
        self.add_option('--pdfdir', init=None,
                type=filepath, check=pdfdir,
                help='pdf documentation', hidden=False,
                help_var='DIR', help_def='DOCDIR')
        self.add_option('--psdir', init=None,
                type=filepath, check=psdir,
                help='ps documentation', hidden=False,
                help_var='DIR', help_def='DOCDIR')
