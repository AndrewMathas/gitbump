#!/usr/bin/env python3

r'''
Usage: git bump [major|minor|patch] [commit message]

Use git bump to:
    - increment the version number stored in the .ini file for the project
    - add a tag to the repository with the  optional commit message


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

class BumpVersion:

    def __init__(self, options):
        pass


# ---------------------------------------------------------------------------
if __name__ == '__main__':
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

    parser.add_argument(
      action  = 'append',
      default = [],
      dest    = 'message',
      nargs   = '*',
      type    = list,
      help    = "Git commit message"
    )

    BumpVersion( parser.parse_args())
