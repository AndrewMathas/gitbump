#!/usr/bin/env python3

r'''
Use git bump to:
    - increment the version number in the .ini file for the project
    - update the release and copyright dates in the .ini file
    - add a tag to the git repository with an optional commit message
    - optionally, push the tags to the remote repository

When a pre-release flag is used when a pre-release flag is already in play then
it is incremented and otherwise, by default, the minor version is incremented
and the pre-release flag is added to it. To create a major pre-release use
`--major` as well. If a pre-release flag is already being used and lower
pre-release flag is used then `git bump` exits with an error.

Author
......

Andrew Mathas
Version {version}
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
'''

import argparse
import datetime
import os
import re
import subprocess
import sys


############################################################
def git(command):
    '''
    Run the git command `cmd` and return the output
    '''
    git = subprocess.run(f'git {command}', shell=True, capture_output=True)
    if git.returncode != 0 or git.stderr.decode() != '':
        if 'spelling errors' not in git.stderr.decode():
            print(f'There was a problem running the git command\n    git {command}')
            print(f'The following error occurred: {git.stderr.decode()}')
            sys.exit(1)

    return git.stdout.decode().strip()


############################################################
class Settings(dict):
    r"""
    A dummy class for reading and storing key-value pairs that are read from a file
    """
    def __init__(self, filename):
        super().__init__()
        with open(os.path.join(os.path.dirname(__file__), filename), 'r') as meta:
            for line in meta:
                key, val = line.split('=')
                if key.strip() != '':
                    setattr(self, key.strip().lower(), val.strip())

settings = Settings('gitbump.ini')


############################################################
class BumpVersion:

    def __init__(self, options):
        '''
        We have to do the following:
            - locate and read the ini file for the project
            - bump the patch/minor/major version
            - save the version number in the ini file
            - add a tag to the git repository with the supplied commit message
            - push the tags to the remote repository

        INPUTS:

        The input `options` must be a dictionary containing the following keys:
            - level      -- the release level: patch, minor or major
            - prerelease -- a pre-release level: alpha, beta or rc (release candidate)
            - message    -- the commit message to use in the repository
            - pushtags   -- when true finish with 'git push --tags'

        '''
        # remember the options
        if options.prerelease is None:
            self.level      = 'patch' if options.level is None else options.level
        else:
            self.level      = 'minor' if options.level is None else options.level
        self.prerelease = options.prerelease
        self.message    = ' '.join(options.message)
        self.pushtags   = options.pushtags

        # read ini file
        self.read_ini_file(options.ini_file)

        # increment the version number
        self.bump_version()

        # save updated ini file
        self.update_ini_file()

        # commit new version and add a tag
        self.add_git_tag()


    def add_git_tag(self):
        '''
        Add a git tag the release together with any commit message
        '''
        description = {
            'major': 'Version',
            'minor': 'Minor update',
            'patch': 'Patch',
        }[self.level]

        if self.message == '':
            git(f'commit -am "{description} {self._ini_file_data["version"]}"')
            git(f'tag -a v{self._ini_file_data["version"]}')
        else:
            git(f'commit -am "{description} {self._ini_file_data["version"]}: {self.message}"')
            git(f'tag -a v{self._ini_file_data["version"]} -m "{self.message}"')

        if self.pushtags:
            git('push --tags')


    def bump_version(self):
        '''
        Bump the version number in self._ini_file_data["version"]

        TODO: support release candidates etc
        '''

        version = re.split('\.|-', self._ini_file_data['version'])
        # enforce semvar version number of the form major.minor.patch
        while len(version) < 3:
            version.append('0')

        # map levels to array indices
        level = {
            'major': 0,
            'minor': 1,
            'patch': 2,
        }[self.level]

        if self.prerelease is None:

            if len(version) == 4:
                # a pre-release is in play so we need to check that we are
                # bumping at the correct level
                if any(version[l]!='0' for l in range(level+1,3)):
                    print(f'A {self.level} release cannot follow pre-release {self._ini_file_data["version"]}')
                    sys.exit(5)

                else:
                    # bump the pre-release to a release in the ini file data
                    self._ini_file_data['version'] = ".".join(version[:3])

            else:
                # straightforward increment of correct level of the version number
                version[level] = f'{int(version[level])+1}'
                # followed by resetting the remaining version numbers
                for l in range(level+1,3):
                    version[l] = '0'

                # store the new version in the ini file data
                self._ini_file_data['version'] = '.'.join(version)

        elif len(version) == 4:
            # a pre-release flag is already in play

            if self.prerelease[0] < version[0]:
                print(f'An {self.prerelease} pre-release cannot follow pre-release {self._ini_file_data["version"]} !')
                sys.exit(4)

            elif self.prerelease[0] == version[0]:
                # increment the pre-release number and store in the ini file data
                version[3] = f'{version[3][0]}{int(version[3][1])+1}'
                self._ini_file_data['version'] = f'{".".join(version[:3])}-{version[3]}'

            else:
                # start the next pre-release from 0 and store in ini file data
                self._ini_file_data['version'] = f'{".".join(version[:3])}-{self.prerelease[0]}0'

        else:
            # increment version number
            version[level] = f'{int(version[level])+1}'
            for l in range(level+1,3):
                version[l] = '0'
            self._ini_file_data['version'] = f'{".".join(version[:3])}-{self.prerelease[0]}0'


    def read_ini_file(self, ini_file):
        '''
        Locate and read the ini file for the project, storing the data
        in the dictionary self._ini_file.
        '''


        if ini_file is None:
            # change directory to the root of the repository
            project_dir = git('root')

            try:
                os.chdir(project_dir)
            except IOError as err:
                print(f'There was a problem changing to the root directory of the project\n - {err}')
                sys.exit(2) 

            project = os.path.basename(project_dir).lower()
            self._ini_file = git(rf'ls-files \*{project}\*.ini')
        else:
            self._ini_file = ini_file if ini_file.endswith('ini') else f'{ini_file}.ini'
            if not os.path.isfile(self._ini_file):
                print(f'ini file "{self._ini_file}" not found!')
                sys.exit(2)

        self._ini_file_data = {}
        try:
            with open(self._ini_file) as ini:
                for line in ini:
                    key, value = line.split('=')
                    self._ini_file_data[key.strip()] = value.strip()

        except FileNotFoundError:
            print('No ini file found in the repository!')
            sys.exit(3)

        if 'version' not in self._ini_file_data:
            print(f'The version number is not specified in {self._ini_file}')
            sys.exit(2)


    def update_ini_file(self):
        '''
        Save the updated ini file
        '''
        # update the release date
        if 'release date' in self._ini_file_data:
            now = datetime.datetime.now().astimezone()
            self._ini_file_data['release date'] = f'{now:%-d %B %Y %Z}'

        # update the copyright date
        if 'copyright' in self._ini_file_data:
            try:
                copyr, extra = self._ini_file_data['copyright'].split(' ')
            except ValueError:
                copyr = self._ini_file_data['copyright']
                extra=''
            now = datetime.datetime.now().astimezone()
            if '-' in copyr:
                one, two = copyr.split('-')
                copyr = f'{one}-{now:%Y}'
            else:
                year = f'{now:%Y}'
                if int(year) < int(copyr):
                    print('Current copyright date is in the future!')
                    sys.exit(6)
                elif copyr != year:
                    copyr = f'{copyr}-{year}'

            self._ini_file_data['copyright'] = copyr if extra=='' else f'{copyr} {extra}'

        padding = max(len(key) for key in self._ini_file_data)
        with open(self._ini_file, 'w') as ini:
            for key in self._ini_file_data:
                ini.write(f'{key:<{padding}s} = {self._ini_file_data[key]}\n')



# ---------------------------------------------------------------------------
def main():
    '''
    Parse command line arguments and pass them to BumpVersion
    '''
    parser = argparse.ArgumentParser(
        add_help=False,
        description='Increment the version number in the ini file for a project and add tags to the repository',
    )

    level = parser.add_mutually_exclusive_group()
    level.add_argument('-p', '--patch',
      action  = 'store_const',
      const   = 'patch',
      default = None,
      dest    = 'level',
      help    = 'increment patch version (default)'
    )
    level.add_argument('-m', '--minor',
      action  = 'store_const',
      const   = 'minor',
      dest    = 'level',
      help    = 'increment minor version'
    )
    level.add_argument('-M', '--major',
      action  = 'store_const',
      const   = 'major',
      dest    = 'level',
      help    = 'increment major version'
    )

    prerelease = parser.add_mutually_exclusive_group()
    prerelease.add_argument('-a', '--alpha',
      action  = 'store_const',
      const   = 'alpha',
      default = None,
      dest    = 'prerelease',
      help    = 'alpha pre-release'
    )
    prerelease.add_argument('-b', '--beta',
      action  = 'store_const',
      const   = 'beta',
      default = None,
      dest    = 'prerelease',
      help    = 'beta pre-release'
    )
    prerelease.add_argument('-r', '--rc',
      action  = 'store_const',
      const   = 'rc',
      dest    = 'prerelease',
      help    = 'release candidate'
    )

    parser.add_argument('-i', '--ini-file',
      default = None,
      help    = 'Specify the name of the ini file to use'
    )

    parser.add_argument('--pushtags',
      action  = 'store_true',
      default = False,
      help    = 'Push the tags to the remote'
    )

    parser.add_argument('-v', '--version',
      action  ='version',
      version = settings.version,
      help    = argparse.SUPPRESS
    )

    # override default help mechanism
    parser.add_argument('-h', '--help',
      default = 0,
      action  = 'count',
      help    = 'use -h for basic usage and -hh for extended help',
    )

    parser.add_argument(
      default = '',
      dest    = 'message',
      nargs   = '*',
      type    = str,
      help    = "Git commit message"
    )

    options = parser.parse_args()

    if options.help > 0:
        parser.print_help()
        if options.help > 1:
            print(__doc__.format(copyright=settings.copyright, version=settings.version))

    else:
        BumpVersion( parser.parse_args() )


if __name__ == '__main__':
    main()
