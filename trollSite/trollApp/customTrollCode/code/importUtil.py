from __future__ import print_function

from fabric.api import env, local, sudo
from json import load
from platform import uname
from sys import argv


def getPlatform():
    return uname()[0]


def login_into_server():
    try:
        jsonFile = "trollApp/customTrollCode/code/localConfig.json"
        jsonData = open(jsonFile, 'r')
        serverConfig = load(jsonData)

    except:
        print("Missing 'localConfig.json' file!")
        print("Aborting Server access immediately")

        import sys
        sys.exit(1)

    try:
        env.hosts.append(serverConfig['server'])
        env.user = serverConfig['username']
        env.password = serverConfig['password']

    except:
        print("Improper configuraton of 'localConfig.json' file!")
        print("Aborting Server access immediately")

        import sys
        sys.exit(1)


def installModules(*modules):
    for module in modules:
        print("Attempting to install {}...".format(module))

        try:
            if getPlatform() != "Windows":
                sudo("pip install {}".format(module))
            else:
                local("pip install {}".format(module))

            print("Successfully installed {}\n".format(module))

        except:
            print("Failed to install {}\n".format(module))

# only when we run the file with the fab command do we want to login
# for sure; otherwise, none of our commands will work
if argv[0] in ('fab-script', '/usr/local/bin/fab'):
    if getPlatform() != "Windows":
        login_into_server()  # will need sudo command

else:
    raise Exception(argv)
