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

def put_line_in_width(file, line, width, indent):
    ''' Print a line with wrapping.
    '''
    line = line.rstrip(' ')
    if len(line) <= width or ' ' not in line.lstrip(' '):
        # this is not just an optimization
        file.writelines([line, '\n'])
        return
    line += ' '
    indents = indent * ' '

    initial_spaces = len(line) - len(line.lstrip(' '))
    while line.lstrip():
        space = line.rfind(' ', initial_spaces, width + 1)
        if space == -1:
            space = line.find(' ', initial_spaces)
        if space == -1:
            space = len(line)
        file.writelines([line[:space], '\n'])
        line = indents + line[space+1:].lstrip(' ')
        initial_spaces = indent


class HelpSection(object):
    ''' A help section contains some header lines and some related options.
    '''
    __slots__ = (
            'headers',
            'options',
    )
    def __init__(self):
        ''' Create an empty help section.
        '''
        self.headers = []
        self.options = []

    def add_text(self, text, hidden):
        ''' Add a header line.
        '''
        self.headers.append((hidden, text))

    def add_option(self, name, text, hidden):
        ''' Add an option with its description.
        '''
        self.options.append((hidden, name, text))

    def print(self, file, hidden, width):
        ''' Format (some of) the help text prettily.
        '''
        if self.options:
            for oh, name, ht in self.options:
                if oh <= hidden:
                    break
            else:
                return False

        # options longer than this will be split into multiple lines
        split_width = width / 4 - 2
        # longest option
        longest_opt = 0
        for oh, name, ht in self.options:
            if oh > hidden:
                continue
            l = len(name) + 2
            if l > split_width:
                continue
            if l > longest_opt:
                longest_opt = l
        if longest_opt == 0:
            longest_opt = int(split_width)

        for oh, ht in self.headers:
            if oh > hidden:
                continue
            put_line_in_width(file, ht, width, 0)

        for oh, name, ht in self.options:
            if oh > hidden:
                continue
            # no, it's not really that simple
            if len(name) > longest_opt:
                file.writelines(['  ', name, '\n'])
                name = ''
            line = '  %-*s%s' % (longest_opt, name, ht)
            put_line_in_width(file, line, width, longest_opt + 2)

        return True


def detect_terminal_width(fd, DEFAULT_WIDTH=float('inf')):
    ''' Detect the width of a terminal.
    '''
    if not isinstance(fd, int):
        fd = getattr(fd, 'fileno', lambda: -1)()
    if fd == -1:
        return DEFAULT_WIDTH

    import fcntl
    import termios
    try:
        buf = fcntl.ioctl(fd, termios.TIOCGWINSZ, b'xx' * 4)
    except IOError as e:
        import errno
        if e.errno != errno.ENOTTY:
            raise
        return DEFAULT_WIDTH
    import struct
    ws_row, ws_col, ws_xpixel, ws_ypixel = struct.unpack('HHHH', buf)
    return ws_col


class Help(object):
    ''' Help collects the set of flavor text and option descriptions
        related to arguments.
    '''
    __slots__ = (
            'sections',
    )
    def __init__(self):
        ''' Help does not take any arguments during construction.
        '''
        self.sections = []

    def add_text(self, help, hidden):
        ''' Add a header line.

            This creates a new section if the last line wasn't a header.
        '''
        if not self.sections or self.sections[-1].options:
            self.sections.append(HelpSection())
        self.sections[-1].add_text(help, hidden)

    def add_option(self, name, help, hidden):
        ''' Add an option with its description to the current section.

            This creates a new section only if it is first.
        '''
        if not self.sections:
            self.sections.append(HelpSection())
        self.sections[-1].add_option(name, help, hidden)

    def print(self, file, hidden, width=0):
        ''' Print all the help at the given level of hidden-ness.
        '''
        if width == 0:
            width = detect_terminal_width(file)
        if width < 20:
            width = 80

        for s in self.sections:
            if s.print(file, hidden, width):
                file.write('\n')
