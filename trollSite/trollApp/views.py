from django.core.mail import send_mail
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from fabric.api import lcd, local
from json import dump
from os import chdir, getcwd
from nltk.corpus import wordnet
from platform import uname
from random import random
from string import maketrans, punctuation
from subprocess import call
from time import time
from trollApp.models import Download, Synonym
from webbrowser import open_new_tab

import re

trollRedirectProb = 0.1
updateFrequency = 0.05
spaces = re.compile(r'\s+')
punctuation = """!"#$%&()*+,-./:;<=>?@[\]^_`{|}~"""

WINDOWS = "Windows"
LINUX = "Linux"
MAC = "Darwin"

def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')

def displayAbout(request):
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        return render(request, 'trollApp/aboutDisplay.html')

def displayDownloads(request):
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            'windows_downloads': Download.objects.filter(target_os=WINDOWS),
            'linux_downloads': Download.objects.filter(target_os=LINUX),
            'mac_downloads': Download.objects.filter(target_os="Mac")
            }
        return render(request, 'trollApp/downloadsDisplay.html', context)

def displayCustomCreate(request):   
    if random() < trollRedirectProb:
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
    
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response

def downloadCustomFile(request):
    trollCode = request.POST.get("code", "")
    trollCode = trollCode.replace("\r\n", "\n")

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
            returnCode = call(["python", "{}/convertToExe.py".format(codeDirectory),
                               "-f", tmpFile], creationflags = CREATE_NO_WINDOW)

        else: # No VM on which to run this conversion yet
            returnCode = 1

    else:
        exeFilename = tmpFile.replace(".py", "")
        if osTarget == sysPlatform: # run locally if possible
            returnCode = call(["python", "{}/convertToExe.py".format(codeDirectory),
                               "-f", tmpFile])
            
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
                
    if returnCode != 0: # fail
        request.session["error_msg"] = "Error in submission! Please try submitting again!"
        request.session["prev_code"] = trollCode
        request.session["os_target"] = osTarget
        
        return HttpResponseRedirect("/trollApp/customCreation")

    wrapper = FileWrapper(open(exeDirectory + exeFilename, 'rb'))
    content_type = "application/x-executable"

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(exeFilename)
    return response

def displaySuggestions(request):
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            "error_msg": request.session.get("error_msg"),
            "prev_email": request.session.get("prev_email")
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
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')   
    else:
        emailBody = request.POST.get("suggestion", "")
        emailSucceed = True
        successCount = 0
        
        try:
            successCount = send_mail("Troll Suggestion", emailBody, "no-reply@trollololer.com",
                                     ['duhtrollmaster@gmail.com'], fail_silently = True)
        except:
            emailSucceed = False
            
        finally:
            if emailSucceed and successCount > 0:
                request.session["error_msg"] = "The Troll Master Thanks You!"
                request.session["prev_email"] = ""

            else: # fail
                request.session["error_msg"] = "Error in submission! Please try submitting again!"
                request.session["prev_email"] = emailBody

            return HttpResponseRedirect("/trollApp/suggestions")

def displayTrollifyEmail(request):
    #if random() < trollRedirectProb:
    if False:
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

        return render(request, 'trollApp/trollifyDisplay.html', context)

def sendTrollifiedEmail(request):
    #if random() < trollRedirectProb:
    if False:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        subject = request.POST.get("subject", "")
        sender = request.POST.get("sender", "")
        receiver = request.POST.get("receiver", "")
        emailBody = request.POST.get("email", "")

        emailSucceed = True
        successCount = 0
        
        try:
            successCount = send_mail(subject, emailBody, receiver,
                                     [sender], fail_silently = True)
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

            else: # fail
                request.session["error_msg"] = "Error in submission! Please try submitting again!"
                request.session["subject"] = subject
                request.session["sender"] = sender
                request.session["receiver"] = receiver
                request.session["troll_email"] = emailBody

        return HttpResponseRedirect("/trollApp/trollifyEmail")
    
def trollifyEmail(request):
    #if random() < trollRedirectProb:
    if False:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        emailBody = request.POST.get("email", "")
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
        
        if random() < updateFrequency:
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
