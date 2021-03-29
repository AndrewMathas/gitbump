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

from gitbump import settings, __doc__

setup(name             = settings.program,
      version          = settings.version,
      description      = settings.description,
      long_description = __doc__.format(copyright=settings.copyright, version=settings.version),
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
