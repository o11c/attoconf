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

class Project(object):
    ''' A Project is a directory and the list of options that can be set.
    '''
    __slots__ = (
            'aliases',
            'options',
            'help',
    )
    def __init__(self, srcdir):
        ''' A Project is initially constructed from just the source directory
        '''

    def add_help(self, text, hidden):
        ''' Directly add a line of text to the help.
        '''

    def add_alias(self, key, expansion, help, hidden):
        ''' Add an alias.

            This is necessary for anything to appear without an =.

            The expansion is a list of other options, which may be aliases.
        '''

    def add_option(self, name, init, type, check, help, hidden):
        ''' Add an actual option.

            This must be passed with a =.

            In the builder, the var will first be set to init.

            If the argument is passed, the type hook is called immediately
            to validate the argument.

            The check hooks will be called at final time,
            in the order they were added.

            Additionally, a line of help is added, with additional formatting.
        '''

class Build(object):
    ''' A Build is a directory and set of options applied to a Project.
    '''
    __slots__ = (
            'project',
            'vars',
    )
    def __init__(self, project, bindir):
        ''' A Build is initially constructed from
        '''

    def apply_arg(self, arg):
        ''' Parse a single argument, expanding aliases.
        '''

    def finish(self):
        ''' With the current set of variables, run all the checks
            and presumably produce some sort of output.
        '''

    def configure(self, args, env):
        ''' Automatically call apply_arg() a bunch of times, then finish().
        '''
