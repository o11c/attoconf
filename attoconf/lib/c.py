#   Copyright 2013-2014 Ben Longbons <b.r.longbons@gmail.com>
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

import errno
import os
import subprocess

from .arches import Arches2
from ..types import ShellList

class TestError(Exception):
    pass

def do_exec(build, args):
    p = subprocess.Popen(args.list, cwd=build.builddir,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
    out, _ = p.communicate()
    retcode = p.wait()
    return retcode, out


class TempFile:
    ''' context manager that optionally creates and then removes a file
    '''
    __slots__ = ('filename')

    def __init__(self, filename, content):
        self.filename = filename
        if content is not None:
            with open(filename, 'wx') as of:
                of.write(content)
        else:
            # TODO: raise OSError(errno.EEXIST) if file already exists
            pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        try:
            os.remove(self.filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise


def try_compile_c(build, body, CFLAGS=[], CPPFLAGS=[]):
    CC = build.vars['CC']
    CFLAGS = build.vars['CFLAGS'] + CFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    in_ = 'atto-test.c'
    ins = [in_]
    out = 'atto-test.o'

    args = CC + CFLAGS + CPPFLAGS + ['-c', '-o', out, in_]
    with TempFile(in_, body), TempFile(out, None):
        status, error = do_exec(build, args)
    if status:
        raise TestError(error)

def try_compile_link_c(build, body, CFLAGS=[], CPPFLAGS=[], LDFLAGS=[], LIBS=[]):
    CC = build.vars['CC']
    CFLAGS = build.vars['CFLAGS'] + CFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
    LIBS = build.vars['LIBS'] + LIBS
    in_ = 'atto-test.c'
    ins = [in_]
    out = 'atto-test'

    args = CC + CFLAGS + CPPFLAGS + LDFLAGS + ins + LIBS + ['-o', out]
    with TempFile(in_, body), TempFile(out, None):
        status, error = do_exec(build, args)
    if status:
        raise TestError(error)

def try_compile_cxx(build, body, CXXFLAGS=[], CPPFLAGS=[]):
    CXX = build.vars['CXX']
    CXXFLAGS = build.vars['CXXFLAGS'] + CXXFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    in_ = 'atto-test.cxx'
    out = 'atto-test.o'

    args = CXX + CXXFLAGS + CPPFLAGS + ['-c', '-o', out, in_]
    with TempFile(in_, body), TempFile(out, None):
        status, error = do_exec(build, args)
    if status:
        raise TestError(error)

def try_compile_link_cxx(build, body, CXXFLAGS=[], CPPFLAGS=[], LDFLAGS=[], LIBS=[]):
    CXX = build.vars['CXX']
    CXXFLAGS = build.vars['CXXFLAGS'] + CXXFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
    LIBS = build.vars['LIBS'] + LIBS
    in_ = 'atto-test.cxx'
    ins = [in_]
    out = 'atto-test'

    args = CXX + CXXFLAGS + CPPFLAGS + LDFLAGS + ins + LIBS + ['-o', out]
    with TempFile(in_, body), TempFile(out, None):
        status, error = do_exec(build, args)
    if status:
        raise TestError(error)

if 0:
    def try_linkonly_c(build, ins, LDFLAGS=[], LIBS=[]):
        CC = build.vars['CC']
        LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
        LIBS = build.vars['LIBS'] + LIBS
        out = 'atto-test'

        args = CC + LDFLAGS + ins + LIBS + ['-o', out]
        with TempFile(out, None):
            status, error = do_exec(build, args)
        if status:
            raise TestError(error)

def try_compile_link2_c(build, body, CFLAGS=[], CPPFLAGS=[], LDFLAGS=[], LIBS=[]):
    CC = build.vars['CC']
    CFLAGS = build.vars['CFLAGS'] + CFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
    LIBS = build.vars['LIBS'] + LIBS
    in_ = 'atto-test.c'
    ins = [in_]
    mid = 'atto-test.o'
    mids = [mid]
    out = 'atto-test'

    args1 = CC + CFLAGS + CPPFLAGS + ['-c', '-o', mid, in_]
    args2 = CC + LDFLAGS + mids + LIBS + ['-o', out]
    with TempFile(mid, None):
        with TempFile(in_, body):
            status, error = do_exec(build, args1)
        if status:
            raise TestError(error)

        with TempFile(out, None):
            status, error = do_exec(build, args2)
        if status:
            raise TestError(error)

if 0:
    def try_linkonly_cxx(build, ins, LDFLAGS=[], LIBS=[]):
        CXX = build.vars['CXX']
        LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
        LIBS = build.vars['LIBS'] + LIBS
        out = 'atto-test'

        args = CXX + LDFLAGS + ins + LIBS + ['-o', out]
        with TempFile(out, None):
            status, error = do_exec(build, args)
        if status:
            raise TestError(error)

def try_compile_link2_cxx(build, body, CXXFLAGS=[], CPPFLAGS=[], LDFLAGS=[], LIBS=[]):
    CXX = build.vars['CXX']
    CXXFLAGS = build.vars['CXXFLAGS'] + CXXFLAGS
    CPPFLAGS = build.vars['CPPFLAGS'] + CPPFLAGS
    LDFLAGS = build.vars['LDFLAGS'] + LDFLAGS
    LIBS = build.vars['LIBS'] + LIBS
    in_ = 'atto-test.cxx'
    ins = [in_]
    mid = 'atto-test.o'
    mids = [mid]
    out = 'atto-test'

    args1 = CXX + CXXFLAGS + CPPFLAGS + ['-c', '-o', mid, in_]
    args2 = CXX + LDFLAGS + mids + LIBS + ['-o', out]
    with TempFile(mid, None):
        with TempFile(in_, body):
            status, error = do_exec(build, args1)
        if status:
            raise TestError(error)

        with TempFile(out, None):
            status, error = do_exec(build, args2)
        if status:
            raise TestError(error)


def ldflags(build, LDFLAGS):
    pass

def libs(build, LIBS):
    # compatibility
    build.vars['LDLIBS'] = LIBS

def cppflags(build, CPPFLAGS):
    pass

def cc(build, CC):
    if CC.list == []:
        HOST = build.vars['HOST']
        if HOST:
            build.vars['CC'].list = [HOST + '-gcc']
        else:
            build.vars['CC'].list = ['gcc']

def cflags(build, CFLAGS):
    try_compile_c(build, 'int main() {}\n')
    try_compile_link_c(build, 'int main() {}\n')
    try_compile_link2_c(build, 'int main() {}\n')

def cxx(build, CXX):
    if CXX.list == []:
        HOST = build.vars['HOST']
        if HOST:
            build.vars['CXX'].list = [HOST + '-g++']
        else:
            build.vars['CXX'].list = ['g++']

def cxxflags(build, CXXFLAGS):
    try_compile_cxx(build, 'int main() {}\n')
    try_compile_link_cxx(build, 'int main() {}\n')
    try_compile_link2_cxx(build, 'int main() {}\n')

class Link(Arches2):
    __slots__ = ()
    def vars(self):
        super(Link, self).vars()
        self.add_option('LDFLAGS', init=[],
                type=ShellList, check=ldflags,
                help='linker flags, e.g. -L<lib dir> if you have libraries in a nonstandard directory <lib dir>',
                hidden=False)
        self.add_option('LIBS', init=[],
                type=ShellList, check=libs,
                help='libraries to pass to the linker, e.g. -l<library>',
                hidden=False)
        self.order.append('LDLIBS') #TODO remove for 1.0

class Preprocess(Arches2):
    __slots__ = ()
    def vars(self):
        super(Preprocess, self).vars()
        self.add_option('CPPFLAGS', init=[],
                type=ShellList, check=cppflags,
                help='C/C++/Objective C preprocessor flags, e.g. -I<include dir> if you have headers in a nonstandard directory <include dir>',
                hidden=False)

class C(Link, Preprocess):
    __slots__ = ()
    def vars(self):
        super(C, self).vars()
        self.add_option('CC', init=[],
                type=ShellList, check=cc,
                help='C compiler command', hidden=False,
                help_def='HOST-gcc')
        self.add_option('CFLAGS', init=['-O2', '-g'],
                type=ShellList, check=cflags,
                help='C compiler flags', hidden=False)

class Cxx(Link, Preprocess):
    __slots__ = ()
    def vars(self):
        super(Cxx, self).vars()
        self.add_option('CXX', init=[],
                type=ShellList, check=cxx,
                help='C++ compiler command', hidden=False,
                help_def='HOST-g++')
        self.add_option('CXXFLAGS', init=['-O2', '-g'],
                type=ShellList, check=cxxflags,
                help='C++ compiler flags', hidden=False)
