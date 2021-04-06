|version|
|pyversion|
|GPL3|

==========
`git_bump`
==========

usage: gitbump.py [-p | -m | -M] [-a | -b | -r] [--pushtags] [-h]
                  [message ...]

Increment the version number in the ini file for a project and add tags to the
repository

positional arguments:
  message      Git commit message

optional arguments:
  -p, --patch  increment patch version
  -m, --minor  increment minor version
  -M, --major  increment major version
  -a, --alpha  alpha pre-release
  -b, --beta   beta pre-release
  -r, --rc     release candidate
  --pushtags   Push the tags to the remote
  -h, --help   use -h for basic usage and -hh for extended help


Use git bump to:
    - increment the version number in the .ini file for the project
    - update the release date in the .ini file
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
Version 0.7.1
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


.. _`git bump`: https://github.com/AndrewAtLarge/gitbump
.. _GPL: http://www.gnu.org/licenses/gpl.html
.. |version| image:: https://img.shields.io/github/v/tag/AndrewAtLarge/gitcat?color=success&label=version
.. |pyversion| image:: https://img.shields.io/badge/requires-python3.9%2B-important
.. |GPL3| image:: https://img.shields.io/badge/license-GPLv3-blueviolet.svg
   :target: https://www.gnu.org/licenses/gpl-3.0.en.html

