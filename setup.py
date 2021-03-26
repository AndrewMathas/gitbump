# -*- encoding: utf-8 -*-

r'''
-----------------------------------------------------------------------------------------
    setup | git-bump setuptools configuration

      - python3 setup.py build    :  build everything needed to install
      - python3 setup.py develop  :  install package in develop mode
      - python3 setup.py upload   :  upload to PyPi

    Copyright (C) Andrew Mathas

    Distributed under the terms of the GNU General Public License (GPL)
                  http://www.gnu.org/licenses/

    <Andrew.Mathas@gmail.com>
-----------------------------------------------------------------------------------------
'''

import os
import subprocess

from setuptools import setup, find_packages

import gitbump

class Settings(dict):
    r"""
    A dummy class for reading and storing key-value pairs that are read from a file
    """
    def __init__(self, filename):
        super().__init__()
        with open(filename, 'r') as meta:
            for line in meta:
                key, val = line.split('=')
                if key.strip() != '':
                    setattr(self, key.strip().lower(), val.strip())

settings = Settings('gitbump.ini')

setup(name             = settings.program,
      version          = settings.version,
      description      = settings.description,
      long_description = gitbump.__doc__,
      author           = settings.author,
      author_email     = settings.author_email,

      keywords         = 'git, version, tags',

      packages=find_packages(),
      python_requires='>=3.7',

      entry_points     = {'console_scripts': ['git-bump = gitbump:main'],},

      license          = settings.licence,
      classifiers      = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7+',
        'Topic :: Software Development :: Version Control :: Git'
      ]
)
