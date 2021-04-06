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

from setuptools import setup, find_packages, Command

from gitbump import settings, __doc__


# ----------------------------------------------------------------------
# Class for building the package readme file and manual
# ----------------------------------------------------------------------

LICENSE='''
Author
......

{author} Mathas

`git bump`_ version {version}

Copyright (C) {copyright}

------------

GNU General Public License, Version 3, 29 June 2007

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License (GPL_) as published by the Free
Software Foundation, either version 3 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU General Public License for more details.

.. _`git bump`: {repository}
.. _GPL: http://www.gnu.org/licenses/gpl.html
.. |version| image:: https://img.shields.io/github/v/tag/AndrewAtLarge/gitcat?color=success&label=version
.. |pyversion| image:: https://img.shields.io/badge/requires-python{python}%2B-important
.. |GPL3| image:: https://img.shields.io/badge/license-GPLv3-blueviolet.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html

'''


class BuildDoc(Command):
    r'''
    Build the README and documentation for git-bump:

    > python3 setup doc
    '''
    description = 'Build the README and manual files'
    user_options = []

    def initialize_options(self):
        '''init options'''
        if not os.path.exists('man/man1'):
            os.makedirs('man/man1')

    def finalize_options(self):
        '''finalize options'''
        pass

    def run(self):
        '''
        This is where all of the work is done
        '''
        self.clean_doc_files()
        self.build_readme()
        self.build_manual()

    def build_readme(self):
        '''
        Construct the README.rst file from the files in the doc directory and
        using gitbump.py --generate_help.
        '''
        doc = __doc__.split('******')
        with open('README.rst', 'w', newline='\n') as readme:
            readme.write(self.readme())

    @staticmethod
    def build_manual():
        '''
        Build the git-bump manual from the README file
        '''
        subprocess.run('rst2html5.py README.rst README.html', shell=True)
        subprocess.run('rst2man.py README.rst man/man1/git-bump.1', shell=True)

    @staticmethod
    def clean_doc_files():
        '''
        remove all generated doc files
        '''
        for doc in ['README.rst', 'README.html', 'man/man1/git-bump.1']:
            try:
                os.remove(doc)
            except FileNotFoundError:
                pass

    def description(self):
        r'''
        Return an rst string for the long description when uploading to PyPI
        '''
        newline = '\n'
        return f'{self.rst_top()}{newline}{__doc__}{self.rst_bottom()}'

    def readme(self):
        r'''
        Return an rst string for the README file
        '''
        newline = '\n'
        return f'{self.rst_top()}{newline}{self.usage_message()}{newline}{__doc__}{self.rst_bottom()}'

    def rst_bottom(self):
        r'''
        Return a string for the bottom the rst file, which includes the licence
        '''
        return LICENSE.format(
                author     = settings.author,
                copyright  = settings.copyright.split(' ')[0],
                python     = settings.python,
                repository = settings.repository,
                version    = settings.version
        )

    def rst_top(self):
        r'''
        Return a string for the top the rst file, which includes the heading
        '''
        newline = '\n'
        return f'{"="*10}{newline}`git_bump`{newline}{"="*10}{newline}'

    def usage_message(self):
        '''
        Return the git-bump usage message generated by argparse
        '''
        with subprocess.Popen('./gitbump.py --help', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pipes:
            output, error = pipes.communicate()
        return output.decode()


# ----------------------------------------------------------------------
# Setup tools configuration
# ----------------------------------------------------------------------

setup(name             = settings.program,
      version          = settings.version,
      description      = settings.description,
      long_description = __doc__.format(copyright=settings.copyright, version=settings.version),
      long_description_content_type='text/x-rst',
      author           = settings.author,
      author_email     = settings.author_email,

      keywords         = 'git, version, tags',

      cmdclass         = {'doc'   : BuildDoc},
      data_files       = [('man/man1', ['man/man1/git-bump.1'])],

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
