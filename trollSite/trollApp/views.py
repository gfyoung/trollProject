from django.core.mail import send_mail
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from fabric.api import lcd, local
from imp import find_module
from json import dump
from nltk.corpus import wordnet
from platform import uname
from random import random
from string import maketrans
from subprocess import call
from time import time
from trollApp.models import ConfigOption, Download, Synonym
from webbrowser import open_new_tab

import re

spaces = re.compile(r'\s+')
punctuation = """!"'#$%&()*+,-./:;<=>?@[\]^_`{|}~"""

emailPattern = """[!?'":#/~`\[\]{}\-\+=\|\(\)\^<>%]"""

WINDOWS = "Windows"
LINUX = "Linux"
MAC = "Darwin"


def getTrollRedirectProb():
    trollRedirectProb = ConfigOption.objects.filter(
        name="trollRedirectProb")[0]
    return float(trollRedirectProb.value)


def getUpdateFrequency():
    updateFrequency = ConfigOption.objects.filter(name="updateFrequency")[0]
    return float(updateFrequency.value)


def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')


def displayAbout(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        return render(request, 'trollApp/aboutDisplay.html')


def displayDownloads(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            'windows_downloads': Download.objects.filter(target_os=WINDOWS),
            'linux_downloads': Download.objects.filter(target_os=LINUX),
            'mac_downloads': Download.objects.filter(target_os="Mac")
            }
        return render(request, 'trollApp/downloadsDisplay.html', context)


def displayCustomCreate(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            "error_msg": request.session.get("error_msg"),
            "prev_code": request.session.get("prev_code"),
            "os_target": request.session.get("os_target")
        }
        request.session["error_msg"] = None
        request.session["prev_code"] = None
        request.session["os_target"] = None

        return render(request, 'trollApp/customCreateDisplay.html', context)


def downloadFile(request, os, filename):
    directory = 'trollApp/trollCode/downloads/'
    wrapper = FileWrapper(open(directory + os + "/" + filename, 'rb'))
    content_type = "application/x-executable"

    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = \
        'attachment; filename={}'.format(filename)
    return response


def moduleExists(module):
    try:
        find_module(module)
        exists = True
    except ImportError:
        exists = False

    return exists


def getMissingImports(code):
    importPattern = re.compile("(?:from .* )?import .*\n*")
    moduleImports = importPattern.findall(code)

    missingImports = set()

    for moduleImport in moduleImports:
        if moduleImport.strip()[:4] == "from":
            module = re.sub("from \s*", "", moduleImport
                            ).split(" ")[0].split(".")[0].strip()
            if module not in missingImports and not moduleExists(module):
                missingImports.add(module)

        else:
            modules = re.sub("import \s*", "", moduleImport).split(",")

            for module in modules:
                module = module.split(".")[0].strip()

                if module not in missingImports and not moduleExists(module):
                    missingImports.add(module)

    return missingImports


def downloadCustomFile(request):
    if request.method == "POST":
        trollCode = request.POST.get("code", "")
        trollCode = trollCode.replace("\r\n", "\n")

        missingImports = getMissingImports(trollCode)
        call(["fab", "-f", "trollApp/customTrollCode/code/importUtil.py",
              "installModules:{}".format(",".join(missingImports))])

        tmpFile = "tmpFile_{}.py".format(int(time()))
        target = open("trollApp/customTrollCode/code/{}".format(tmpFile), "w")
        target.write(trollCode)
        target.close()

        codeDirectory = 'trollApp/customTrollCode/code/'
        exeDirectory = 'trollApp/customTrollCode/downloads/'
        remoteDirectory = 'trollApp/customTrollCode/code/remote/'

        osTarget = request.POST.get("OS")
        sysPlatform = getPlatform()

        if osTarget == WINDOWS:
            exeFilename = tmpFile.replace(".py", ".exe")
            if osTarget == sysPlatform:
                CREATE_NO_WINDOW = 0x08000000
                returnCode = call(["python",
                                   "{}/convertToExe.py".format(codeDirectory),
                                   "-f", tmpFile],
                                  creationflags=CREATE_NO_WINDOW)

            else:  # No VM on which to run this conversion yet
                returnCode = 1

        else:
            exeFilename = tmpFile.replace(".py", "")
            if osTarget == sysPlatform:  # run locally if possible
                returnCode = call(["python",
                                   "{}/convertToExe.py".format(codeDirectory),
                                   "-f",
                                   tmpFile])

            else:
                returnCode = 0
                if osTarget == LINUX:
                    serverConfigFile = "linuxConfig.json"

                elif osTarget == MAC:
                    serverConfigFile = "macConfig.json"

                else:
                    raise Exception("Unknown OS Target: {}".format(osTarget))

                with lcd(remoteDirectory):
                    local("cp {} serverConfig.json".format(serverConfigFile))

                    target = open(remoteDirectory + "tmpFileConfig.json", "w")
                    tmpFileConfig = {"tmpFile": tmpFile}
                    dump(tmpFileConfig, target)
                    target.close()

                    local("fab convert_to_exe")

        if returnCode != 0:  # fail
            request.session["error_msg"] = "Error in submission!" \
                                           " Please try submitting again!"
            request.session["prev_code"] = trollCode
            request.session["os_target"] = osTarget

            return HttpResponseRedirect("/trollApp/customCreation")

        wrapper = FileWrapper(open(exeDirectory + exeFilename, 'rb'))
        content_type = "application/x-executable"

        response = HttpResponse(wrapper, content_type=content_type)
        response['Content-Disposition'] = \
            'attachment; filename={}'.format(exeFilename)
        return response


def displaySuggestions(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            "error_msg": request.session.get("error_msg"),
            "prev_email": request.session.get("prev_email"),
            "subject": request.session.get("subject", ""),
            "sender": request.session.get("sender", "")
        }
        request.session["error_msg"] = None
        request.session["prev_email"] = None

        return render(request, 'trollApp/suggestionsDisplay.html', context)


def getPlatform():
    return uname()[0]


def playTrollSong(request):
    troll_song = "https://www.youtube.com/watch?v=o1eHKf-dMwo"
    open_new_tab(troll_song)
    return HttpResponse("Success!")


def sendSuggestion(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        if request.method == "POST":
            emailBody = sanitizeEmail(request.POST.get("suggestion", ""))
            subject = request.POST.get("subject", "")
            sender = request.POST.get("sender", "")

            emailSucceed = True
            successCount = 0

            try:
                successCount = send_mail(
                    "Troll Suggestion" if subject == "" else subject,
                    emailBody,
                    "no-reply@trollololer.com" if sender == "" else sender,
                    ['duhtrollmaster@gmail.com'], fail_silently=True)
            except:
                emailSucceed = False

            finally:
                if emailSucceed and successCount > 0:
                    request.session["error_msg"] = \
                        "The Troll Master Thanks You!"
                    request.session["prev_email"] = ""
                    request.session["subject"] = ""
                    request.session["sender"] = ""

                else:  # fail
                    request.session["error_msg"] = \
                        "Error in submission! Please try submitting again!"
                    request.session["prev_email"] = emailBody
                    request.session["subject"] = subject
                    request.session["sender"] = sender

                return HttpResponseRedirect("/trollApp/suggestions")


def displayTrollifyEmail(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            "error_msg": request.session.get("error_msg", ""),
            "orig_email": request.session.get("orig_email", ""),
            "troll_email": request.session.get("troll_email", ""),
            "subject": request.session.get("subject", ""),
            "sender": request.session.get("sender", ""),
            "receiver": request.session.get("receiver", ""),
        }

        request.session["error_msg"] = ""
        request.session["orig_email"] = ""
        request.session["troll_email"] = ""
        request.session["subject"] = ""
        request.session["sender"] = ""
        request.session["receiver"] = ""

        return render(request, 'trollApp/trollifyDisplay.html', context)


def sendTrollifiedEmail(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        if request.method == "POST":
            subject = request.POST.get("subject", "")
            sender = request.POST.get("sender", "")
            receiver = request.POST.get("receiver", "")
            emailBody = sanitizeEmail(request.POST.get("trollEmail", ""))

            emailSucceed = True
            successCount = 0

            try:
                successCount = send_mail(subject, emailBody, receiver,
                                         [sender], fail_silently=True)
            except:
                emailSucceed = False

            finally:
                if emailSucceed and successCount > 0:
                    request.session["error_msg"] = "Email Successfully Sent!"
                    request.session["orig_email"] = ""
                    request.session["troll_email"] = ""
                    request.session["subject"] = ""
                    request.session["sender"] = ""
                    request.session["receiver"] = ""

                else:  # fail
                    request.session["error_msg"] = \
                        "Error in submission! Please try submitting again!"
                    request.session["subject"] = subject
                    request.session["sender"] = sender
                    request.session["receiver"] = receiver
                    request.session["troll_email"] = emailBody

            return HttpResponseRedirect("/trollApp/trollifyEmail")


def trollifyEmail(request):
    if random() < getTrollRedirectProb():
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        if request.method == "POST":
            emailBody = sanitizeEmail(request.POST.get("origEmail", ""))
            request.session["orig_email"] = emailBody

            words = set(emailBody.split(" "))

            for word in words:
                cleanWord = sanitizeWord(word)
                emailBody = emailBody.replace(
                    cleanWord, getSynonym(cleanWord))

            request.session["troll_email"] = emailBody

            return HttpResponseRedirect("/trollApp/trollifyEmail")


def getSynonym(word):
    if not word:
        return word

    currentSyns = Synonym.objects.filter(word=word)

    if currentSyns:
        bestSynObj = currentSyns[0]
        bestSyn = bestSynObj.synonym

        if random() < getUpdateFrequency():
            bestSyn = getBestSynonym(word, curSyn=bestSyn)
            bestSynObj.synonym = bestSyn
            bestSynObj.save()

    else:
        bestSyn = getBestSynonym(word)
        bestSynObj = Synonym(word=word, synonym=bestSyn)
        bestSynObj.save()

    return bestSyn


def getBestSynonym(word, curSyn=""):
    if not word:
        return word

    allSyns = wordnet.synsets(word)

    if not allSyns:
        if curSyn:
            return curSyn

        return word

    else:
        bestSyn = curSyn

        for synset in allSyns:
            for possSyn in synset.lemma_names():
                if len(possSyn) > len(bestSyn):
                    bestSyn = possSyn

    return bestSyn


def sanitizeWord(word):
    return str(word).translate(maketrans("", ""), punctuation)


def sanitizeEmail(email):
    return re.sub(emailPattern, "", email)
