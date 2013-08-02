#!/usr/bin/env python

from distutils.core import setup

setup(
    name='attoconf',
    version='1.0',
    description='A small and sensible replacement for GNU autoconf',
    author='Ben Longbons',
    author_email='b.r.longbons@gmail.com',
    url='http://github.com/o11c/attoconf',
    packages=[
        'attoconf',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Software Development :: Build Tools',
    ],
)
