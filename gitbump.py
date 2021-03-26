#!/usr/bin/env python3

r'''
Usage: git bump [major|minor|patch] [commit message]

Use git bump to:
    - increment the version number stored in the .ini file for the project
    - add a tag to the repository with the optional commit message
    - push the tags to the remote repository

Author
......

Andrew Mathas

git bump Version 1.0

Copyright (C) 2021

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
import os
import subprocess
import sys

def git(command):
    '''
    Run the git command `cmd` and return the output
    '''
    git = subprocess.run(f'git {command}', shell=True, capture_output=True)
    if git.returncode != 0 or git.stderr.decode() != '':
        print(f'There was a problem running the git command\n    git {command}')
        print(f'The following error occurred: {git.stderr.decode()}')
        sys.exit(1)

    return git.stdout.decode().strip()

class BumpVersion:

    def __init__(self, options):
        '''
            We have to the following:
                - locate and read the ini file for the project
                - bump the patch/minor/major version
                - save the version number in the ini file
                - add a tag to the git repository with the supplied commit message
                - push the tags to the remote repository
        '''
        # change directory to the root of the repository

        project_dir = git('root')

        try:
            os.chdir(project_dir)

        except IOError as err:
            print(f'There was a problem changing to the root directory of the project\n - {err}')
            sys.exit(2)

        self.level = options.level
        self.commit_message = ' '.join(options.message)
        self.push_tags = options.pushtags

        self.project = os.path.basename(project_dir).lower()
        self.read_ini_file()
        self.bump_version()
        self.save_ini_file()
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

        if self.commit_message == '':
            git(f'commit -am "{description} {self._ini_file_data["version"]}"')
            git(f'tag -a v{self._ini_file_data["version"]}')
        else:
            git(f'commit -am "{description} {self._ini_file_data["version"]}: {self.commit_message}"')
            git(f'tag -a v{self._ini_file_data["version"]} -m "{description}: {self.commit_message}"')

        if self.push_tags:
            git('push --tags')


    def bump_version(self):
        '''
        Bump the version number in self._ini_file_data["version"]

        TODO: support release candidates etc
        '''

        version = self._ini_file_data['version'].split('.')
        # enforce semvar version number of the form major.minor.patch
        while len(version) < 3:
            version.append('0')

        # map levels to array indices
        level = {
            'major': 0,
            'minor': 1,
            'patch': 2,
        }[self.level]

        version[level] = f'{int(version[level])+1}'

        # save the new version in the ini file
        self._ini_file_data['version'] = '.'.join(version)


    def read_ini_file(self):
        '''
        Locate and read the ini file for the project, storing the data
        in the dictionary self._ini_file.
        '''
        self._ini_file = git(rf'ls-files \*{self.project}.ini')
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


    def save_ini_file(self):
        '''
        Save the updated ini file
        '''
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
        description='Increment the version number in the ini file for a project and add tags to the repository',
    )

    level = parser.add_mutually_exclusive_group()
    level.add_argument('-p', '--patch',
      action  = 'store_const',
      const   = 'patch',
      default = 'patch',
      dest    = 'level',
      help    = 'increment patch version'
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

    parser.add_argument('--pushtags',
      action  = 'store_true',
      default = False,
      help    = 'Push the tags to the remote'
    )

    parser.add_argument(
      default = '',
      dest    = 'message',
      nargs   = '*',
      type    = str,
      help    = "Git commit message"
    )

    BumpVersion( parser.parse_args())


if __name__ == '__main__':
    main()
