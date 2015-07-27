from fabric.api import local
from optparse import OptionParser
from os import chdir, getcwd, listdir
from platform import uname
from sqlite3 import connect

DATABASE = "../../../db.sqlite3"
TABLE = "trollApp_download"
MIGRATION = "../migration.txt"

def createSetupFile(filename):
    target = open('setup.py', 'w')
    target.write(
"""
from setuptools import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows = [{'script': '%s'}],
    zipfile = None
)
""" % filename)
    target.close()

def fileExists(filename):
    return filename in listdir(getcwd())

def getPlatform():
    return uname()[0]

def isPythonFile(filename):
    if type(filename).__name__ != "str":
        return False

    filenameParts = filename.split(".")
    return len(filenameParts) == 2 and filenameParts[-1] == "py"

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", type="string", dest="fname",
                      action="append", help="filename(s)")
    parser.add_option("-d", "--descr", type="string", dest="descr",
                      action="append", help="filename description")
    parser.add_option("-n", "--new", action="store_true", dest="make_new",
                      default=False, help="make new download entry")
    opt, args = parser.parse_args()

    if not opt.fname:
        print "No file specified for conversion"

    else:      
        filename = opt.fname[0]
        if isPythonFile(filename):
            if fileExists(filename):
                platform = getPlatform()
                if platform != 'Windows':
                    executable = filename.replace(".py", "")
                    if platform == "Darwin":
                        platform = "Mac"
                        
                    local("pyinstaller -w -F {}".format(filename))
                    local("cp dist/{executable} ../downloads/{platform}/{executable}"
                          .format(executable=executable, platform=platform))
                    local("rm {}.spec".format(executable))
                    local("rm -r build")
                    local("rm -r dist")
                    
                else:
                    executable = filename.replace(".py", ".exe")
                    createSetupFile(filename)
                    local("python setup.py")
                    local("cp dist/{executable} ../downloads/Windows/{executable}"
                          .format(executable=executable))
                    local("rm setup.py")
                    local("rm -r build")
                    local("rm -r dist")

                if opt.make_new:
                    if opt.descr:
                        descr = opt.descr[0]
                        conn = connect(DATABASE)
                        nextId = conn.execute("SELECT COALESCE(MAX(id), 0) " +
                                              "FROM {}".format(TABLE)).fetchone()[0] + 1
                        cmd = "INSERT INTO {} VALUES ({}, '{}', '{}', '{}')".format(
                            TABLE, nextId, platform, executable, descr)
                        conn.execute(cmd)
                        conn.commit()
                        conn.close()

                        target = open("../migration.txt", "a")
                        target.write(cmd + "\n")
                        target.close()
                    else:
                        print "No description provided for file, so no new entry was added"
                    
            else:
                print "File does not exist"
                
        else:
            print "Invalid file for conversion!"
