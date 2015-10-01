#   Copyright 2013-2015 Ben Longbons <b.r.longbons@gmail.com>
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

from .core import Project, Build

class PolymorphicSlotMergerMetaclass(type):

    def __new__(meta, name, bases, dct):
        if '__slots__' not in dct:
            s = ()
            for b in bases:
                s2 = b.__dict__.get('_merge_slots_', ())
                if isinstance(s2, basestring):
                    s2 = (s2,)
                s += s2
            s += dct.get('_merge_slots_', ())
            dct['__slots__'] = s
        else:
            assert dct['__slots__'] == ()
        return type.__new__(meta, name, bases, dct)

    # TODO: remove *args for 1.0
    def __call__(cls, *args, **kwargs):
        instance = type.__call__(cls, *args, **kwargs)
        if 'package' in kwargs or not isinstance(instance,
                __import__('attoconf.lib.install', fromlist=['Install']).Install):
            instance._do_jiggle()
        return instance


# TODO: remove this for 1.0
def add_slots(cls):
    return cls

class ClassyProject(Project):
    ''' A more convenient, objectish, way of setting up a project.
    '''
    __slots__ = ()
    _merge_slots_ = ()
    __metaclass__ = PolymorphicSlotMergerMetaclass

    def __init__(self, srcdir):
        super(ClassyProject, self).__init__(srcdir)

    # TODO: remove this for 1.0
    def jiggle(self):
        pass

    def _do_jiggle(self):
        self.order.append(None)
        self.general()
        self.order.append(None)
        self.paths()
        self.order.append(None)
        self.arches()
        self.order.append(None)
        self.vars()
        self.order.append(None)
        self.features()
        self.order.append(None)
        self.packages()
        self.order.append(None)

        if 0:
            self.tests()
            self.order.append(None)
        self.post()
        self.order.append(None)

    def general(self):
        ''' Registration hook for general options (usually unneeded).
        '''
        self.add_help('General:', hidden=False)
        self.add_alias('--help', ['--help=default'],
                help='display standard help, then exit', hidden=False)
        self.add_option('--help', init='none',
                type=self.do_help, check=None,
                help='just display some kind of help instead of configuring', hidden=False,
                help_var='KIND')
        self.help.add_option('--help=hidden',
                help='display help you should never ever ever care about',
                hidden=False)

    def paths(self):
        ''' Registration hook for path-related options.
            (--prefix, --bindir, etc)

            Probably only used by attoconf.lib.install.
        '''

    def arches(self):
        ''' Registration hook for arch-related options.
            (--build, --host, and sometimes --target)

            Typically this changes the prefix of the compiler.
        '''

    def vars(self):
        ''' Environment variables (usually capital, don't start with a --).

            Usually there is one or two of these for every program needed.
        '''
        self.add_help('Environment Variables:', hidden=False)

    def features(self):
        ''' Customizations for this package (--enable-*).
        '''
        self.add_help('Optional Features:', hidden=False)
        # TODO add '--disable-option-checking'
        self.help.add_option('--disable-FEATURE',
                help='do not include FEATURE (same as --enable-FEATURE=no)',
                hidden=False)
        self.help.add_option('--enable-FEATURE',
                help='include FEATURE (same as --enable-FEATURE=yes)',
                hidden=False)

    def packages(self):
        ''' Settings related to dependencies (--with-*).
        '''
        self.add_help('Optional Packages:', hidden=False)
        self.help.add_option('--with-PACKAGE',
                help='use PACKAGE (same as --with-PACKAGE=yes)',
                hidden=False)
        self.help.add_option('--without-PACKAGE',
                help='do not use PACKAGE (same as --with-PACKAGE=no)',
                hidden=False)

    if 0: # not sure if really needed
        def tests(self):
            ''' Late tests, but still before post.

            '''

    def post(self):
        ''' Special hook for things that need to be done at the very end.

            attoconf.post.make
        '''

    # okay, no more registration hooks
    def build(self, bindir):
        return Build(self, bindir)
