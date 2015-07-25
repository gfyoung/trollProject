from django.core.mail import send_mail
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from mimetypes import guess_type
from platform import uname
from random import random
from subprocess import call
from time import time
from webbrowser import open_new_tab

trollRedirectProb = 0.0

# TODO: Consider making a Model class if the number of examples become massive
class Download(object):
    def __init__(self, filename, description):
        # currently, all downloads are .exe files
        self.shortname = filename.replace('.exe', '')
        self.filename = filename
        self.description = description

    def __unicode__(self):
        return "{}: {}".format(self.filename, self.description)
    
def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')

def displayAbout(request):
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        return render(request, 'trollApp/aboutDisplay.html')

# TODO: Remove the first download when you have an 'official' release
def displayDownloads(request):
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {'downloads' :
                   [Download('displaySuccessCall.exe','Test Download'),
                    Download('infiniteTrollSongLoop.exe', 'Troll Song Infinite Loop'),
                    Download('persistentTkCall.exe', 'Persistent Tkinter Display'),
                    Download('massiveFileWriteCall.exe', 'Write a Ton of Useless Files')]
                   }
        return render(request, 'trollApp/downloadsDisplay.html', context)

def displayCustomCreate(request):   
    if random() < trollRedirectProb:
        return render(request, 'trollApp/trollRedirectDisplay.html')
    else:
        context = {
            "error_msg": request.session.get("error_msg"),
            "prev_code": request.session.get("prev_code")
        }
        request.session["error_msg"] = None
        request.session["prev_code"] = None

        return render(request, 'trollApp/customCreateDisplay.html', context)

def downloadFile(request, filename):
    directory = 'trollApp/trollCode/downloads/'
    wrapper = FileWrapper(open(directory + filename, 'rb'))
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
    
    if getPlatform() == "Windows":
        CREATE_NO_WINDOW = 0x08000000
        exeFilename = tmpFile.replace(".py", ".exe")
        returnCode = call(["python", "{}/convertToExe.py".format(codeDirectory),
                           "-f", tmpFile], creationflags = CREATE_NO_WINDOW)

    else:
        exeFilename = tmpFile.replace(".py", "")
        returnCode = call(["python", "{}/convertToExe.py".format(codeDirectory),
                          "-f", tmpFile])

    if returnCode != 0: # fail
        request.session["error_msg"] = "Error in submission! Please try submitting again!"
        request.session["prev_code"] = trollCode
        
        return HttpResponseRedirect("/trollApp/customCreation")

    call(["chmod", "u+x", exeDirectory + exeFilename])
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
        request.session["prev_emails"] = None
        
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
