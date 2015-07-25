from fabric.api import cd, env, get, local, put, run
from json import load
from sys import argv

codeDirectory = 'trollApp/customTrollCode/code/'
exeDirectory = 'trollApp/customTrollCode/downloads/'
    
def login_into_server():
    try:
        jsonFile = "serverLogin.json"
        jsonData = open(jsonFile, 'r')
        convertData = load(jsonData)

    except:
        print "Missing 'serverLogin.json' file!"
        print "Aborting Server access immediately"
    
        import sys
        sys.exit(1)

    try:
        env.hosts.append(convertData['server'])
        env.user = convertData['username']
        env.password = convertData['password']

    except:
        print "Improper configuraton of 'serverLogin.json' file!"
        print "Aborting Server access immediately"

        import sys
        sys.exit(1)
        
def convert_to_exe():
    jsonFile = "convertData.json"
    jsonData = open(jsonFile, 'r')
    convertData = load(jsonData)
    
    try:
        jsonFile = "convertData.json"
        jsonData = open(jsonFile, 'r')
        convertData = load(jsonData)

    except:
        print "Missing 'convertData.json' file!"
        print "Aborting Server access immediately"
    
        import sys
        sys.exit(1)

    try:
        tmpFile = convertData['tmpFile']
        homeDir = convertData['homeDir']
        exeFile = tmpFile.replace(".py", "")
        
    except:
        print "Improper configuraton of 'convertData.json' file!"
        print "Aborting Server access immediately"


        import sys
        sys.exit(1)

    with cd(homeDir):
        local("cp ../{tmpFile} {tmpFile}".format(tmpFile=tmpFile))

        put(tmpFile, codeDirectory + tmpFile)
        run("python " + codeDirectory + "convertToExe.py -f " + tmpFile)
        get(exeDirectory + exeFile, exeFile)
        
        local("cp {exeFile} ../../downloads/{exeFile}".format(exeFile=exeFile))
        local("rm {} {}".format(tmpFile, exeFile))
        
# only when we run the file with the fab command do we want to login
# for sure; otherwise, none of our commands will work
if 'fab-script' in argv[0]:
    login_into_server()
