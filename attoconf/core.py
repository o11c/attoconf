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

from collections import namedtuple, OrderedDict
import os
import sys

from .help import Help

# Nothing to see here. Move along.
Option = namedtuple('Option', ['type', 'init'])
class ArgumentError(Exception): pass

def as_var(name):
    return name.lstrip('-').replace('-', '_').upper()

def trim_trailing_slashes(path):
    p, s = os.path.split(path)
    if not s:
        return p
    return path

class Project(object):
    ''' A Project is a directory and the list of options that can be set.
    '''
    __slots__ = (
            'srcdir',
            'aliases',
            'options',
            'help',
            'order',
            'checks',
    )
    def __init__(self, srcdir):
        ''' A Project is initially constructed from just the source directory
        '''
        self.srcdir = trim_trailing_slashes(srcdir)
        self.aliases = {}
        self.options = {}
        self.help = Help()
        self.order = []
        self.checks = []

    def add_help(self, text, hidden):
        ''' Directly add a line of text to the help.
        '''
        self.help.add_text(text, hidden)

    def add_alias(self, key, expansion, help, hidden):
        ''' Add an alias.

            This is necessary for anything to appear without an =.

            The expansion is a list of other options, which may be aliases.
        '''
        if key in self.aliases:
            raise KeyError(key)
        expansion = list(expansion)
        self.aliases[key] = expansion
        if help is None:
            help = 'alias for ' + ' '.join(expansion)
        self.help.add_option(key, help, hidden)

    def add_option(self, name, init, type, check,
            help, hidden,
            help_var=None, help_def=None):
        ''' Add an actual option.

            This must be passed with a =.

            In the builder, the var will first be set to init.

            If the argument is passed, the type hook is called immediately
            to validate the argument.

            The check hooks will be called at final time,
            in the order they were added.

            Additionally, a line of help is added, with additional formatting.
        '''
        if name in self.options:
            raise KeyError(name)
        var = as_var(name)
        if check is not None:
            assert type.__module__ == 'attoconf.types'
        else:
            # used by some tests ... should this be fixed there instead?
            if help_var is None:
                help_var = var
        assert init is not None
        init = type(init)
        assert init is not None
        self.options[name] = Option(init=init, type=type)
        if check is not None:
            self.order.append(var)
            self.checks.append(
                    lambda bld: check(bld, **{help_var: bld.vars[var]}))

        if help_var is None:
            help_var = var

        if help_def is None:
            help_def = init
        assert help_def is not None
        help = '%s [%s]' % (help, help_def)

        if help_var != name:
            help_opt = '%s=%s' % (name, help_var)
        else:
            help_opt = name
        self.help.add_option(help_opt, help, hidden)

    def do_help(self, opt):
        ''' Pseudo type-hook to be registered for --help (calls sys.exit).
        '''
        if opt == 'none':
            return opt
        if opt == 'default':
            hidden = False
        elif opt == 'hidden':
            hidden = True
        else:
            raise ValueError('Unknown value for opt: %r' % opt)
        self.help.print(sys.stdout, hidden)
        sys.exit()
# sneaky
Project.do_help.im_func.__module__ = 'attoconf.types'

class Build(object):
    ''' A Build is a directory and set of options applied to a Project.
    '''
    __slots__ = (
            'builddir',
            'project',
            'vars',
            '_seen_args',
    )
    def __init__(self, project, builddir):
        ''' A Build is initially constructed from a project and a build dir.
        '''
        self.project = project
        self.builddir = trim_trailing_slashes(builddir)
        self.vars = {as_var(k): o.init
                for (k, o) in project.options.iteritems()}
        self._seen_args = OrderedDict()

    def apply_arg(self, arg):
        ''' Parse a single argument, expanding aliases.
        '''
        alias = self.project.aliases.get(arg)
        if alias is not None:
            for e in alias:
                # TODO: catch recursive aliases
                # or should they be caught earlier?
                self.apply_arg(e)
            return

        if '=' not in arg:
            if arg in self.project.options:
                raise ArgumentError('Option %s requires an argument' % arg)
            elif arg.startswith('-'):
                raise ArgumentError('Unknown option %s' % arg)
            else:
                raise ArgumentError('Unknown environment variable %s' % arg)

        k, a = arg.split('=', 1)
        if k in self._seen_args:
            del self._seen_args[k]
        self._seen_args[k] = a
        opt = self.project.options.get(k)
        if opt is None:
            raise sys.exit('Unknown option %s' % k)
        self.vars[as_var(k)] = opt.type(a)

    def finish(self):
        ''' With the current set of variables, run all the checks
            and presumably produce some sort of output.
        '''
        for check in self.project.checks:
            check(self)
        status_file = os.path.join(self.builddir, 'config.status')
        # open fd to control +x mode
        status_fd = os.open(status_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0777)
        with os.fdopen(status_fd, 'w') as status:
            print('Generating config.status')
            status.write('#!%s\n' % sys.executable)
            status.write('import os\n')
            status.write('import sys\n')
            status.write('old_build_dir = os.path.dirname(sys.argv[0])\n')
            status.write('configure = os.path.join(old_build_dir, %r, "configure")\n'
                    % self.relative_source())
            seen_args = ['='.join(kv) for kv in self._seen_args.iteritems()]
            status.write('os.execvp(configure, [configure] + %r + sys.argv[1:])\n'
                    % seen_args)

    def configure(self, args, env):
        ''' First apply variables from the environment,
            then call apply_arg() a bunch of times, then finish().
        '''
        for k in self.project.options:
            if k != as_var(k):
                continue
            val = env.get(k)
            if val is not None:
                self._seen_args[k] = val
                opt = self.project.options[k]
                self.vars[as_var(k)] = opt.type(val)

        for arg in args:
            self.apply_arg(arg)

        self.finish()

    def relative_source(self):
        ''' Return a relative path from the build tree to the source tree.
        '''
        srcdir = self.project.srcdir
        builddir = self.builddir
        if os.path.isabs(srcdir) or os.path.isabs(builddir):
            return os.path.realpath(srcdir)
        return os.path.relpath(os.path.realpath(srcdir),
                os.path.realpath(builddir))
