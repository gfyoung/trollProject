from fabric.api import local
from optparse import OptionParser
from os import chdir, getcwd, listdir
from platform import uname


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
            zipfile = None)
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
    opt, args = parser.parse_args()

    if not opt.fname:
        print "No file specified for conversion"

    else:
        codeDirectory = "trollApp/customTrollCode/code"
        chdir(codeDirectory)

        filename = opt.fname[0]
        executable = filename.replace(".py", "")

        if isPythonFile(filename):
            if fileExists(filename):
                if getPlatform() != 'Windows':
                    local("pyinstaller -w -F {}".format(filename))
                    local("cp dist/{} ../downloads/{}".format(
                        executable, executable))
                    local("rm {}.spec".format(executable))
                    local("rm -r build")
                    local("rm -r dist")
                else:
                    createSetupFile(filename)
                    local("python setup.py")
                    local("cp dist/{} ../downloads/{}".format(
                        executable, executable))
                    local("rm setup.py")
                    local("rm -r build")
                    local("rm -r dist")
            else:
                print "File does not exist"
        else:
            print "Invalid file for conversion!"
