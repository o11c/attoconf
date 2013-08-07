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
from pipes import quote as shell_quote
from shlex import split as shell_split

from .core import trim_trailing_slashes


class IntRange(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __call__(self, s):
        i = int(s)
        if self.min <= i <= self.max:
            return i
        raise ValueError('%d is out of range' % i)

sint = IntRange(float('-inf'), float('inf'))
uint = IntRange(0, float('inf'))


class enum(object):
    __slots__ = ('args',)

    def __init__(self, *args):
        self.args = args

    def __call__(self, s):
        if s in self.args:
            return s
        raise ValueError('%r not in {%s}' % (s, ', '.join(self.args)))


class ShellList(object):
    ''' An argument type representing a sequence of 0 or more arguments
    '''
    __slots__ = ('list',)
    def __init__(self, arg):
        if isinstance(arg, str):
            self.list = shell_split(arg)
        elif isinstance(arg, list):
            self.list = arg[:]
        elif isinstance(arg, ShellList):
            self.list = arg.list[:]
        else:
            raise TypeError('arg is an instance of %s' % type(arg).__name__)

    def __str__(self):
        return ' '.join(shell_quote(a) for a in self.list)

    def __add__(self, other):
        if isinstance(other, str):
            other = shell_split(other)
        elif isinstance(other, ShellList):
            other = other.list
        elif not isinstance(other, list):
            raise TypeError('arg is an instance of %s' % type(arg).__name__)
        return ShellList(self.list + other)


def shell_word(s):
    if s != shell_quote(s):
        raise ValueError('not a word: %r' % s)
    return s


def shell_partial_word(s):
    if s == '':
        return s
    return shell_word(s)


def quoted_string(s):
    return shell_quote(s)


def filepath(s):
    s = trim_trailing_slashes(s)
    # must be absolute *and* canonical
    if s != os.path.abspath(s):
        raise ValueError('Not an absolute, canonical pathname: %s' % s)
    return s


def triple(s):
    # Triples do not, in fact, follow a regular pattern.
    # Some have only two segments, some appear to have four ...
    # Also, sometimes a wrong thing is used as a triple.
    # All we *really* care about is generating the tool names.
    if s.startswith('-') or s.endswith('-') or '-' not in s[1:-1]:
        raise ValueError('Probably not a triple')
    return s
