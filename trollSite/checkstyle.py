"""
Runs basic checkstyle on the entire codebase using the PEP8 convention.
Note that this file is self-reflective, so checkstyle will also be run
on the checkstyle.py file itself!
"""

from fabric.api import hide, local
from os import getcwd
from sys import exit

try:
    import pep8
except ImportError:
    print "\nATTENTION: Please install pep8 before running 'checkstyle.py'\n"
    exit(-1)

currentDir = getcwd()

try:
    with hide('aborts', 'running'):
        local("pep8 {projDir} > styleErrors.txt".format(projDir=currentDir))
        print "\nSUCCESS: Checkstyle passed!\n"
except:
    print "\nATTENTION: Checkstyle errors were found!\n" \
          "Please look at {projDir}/styleErrors.txt for " \
          "more information\n".format(projDir=currentDir)
