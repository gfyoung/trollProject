from django.core.mail import send_mail
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from mimetypes import guess_type
from subprocess import call
from time import time

# TODO: Consider making a Model class if the number of examples become massive
class Download(object):
    def __init__(self, filename, description):
        self.filename = filename
        self.description = description

    def __unicode__(self):
        return "{}: {}".format(self.filename, self.description)
    
def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')

def displayAbout(request):
    return render(request, 'trollApp/aboutDisplay.html')

# TODO: Remove the first download when you have an 'official' release
def displayDownloads(request):
    context = {'downloads' :
               [Download('displaySuccessCall.exe','Test Download'),
                Download('infiniteTrollSongLoop.exe', 'Troll Song Infinite Loop'),
                Download('persistentTkCall.exe', 'Persistent Tkinter Display'),
                Download('massiveFileWriteCall.exe', 'Write a Ton of Useless Files')]
               }
    return render(request, 'trollApp/downloadsDisplay.html', context)

def displayCustomCreate(request):
    return render(request, 'trollApp/customCreateDisplay.html')

def downloadFile(request, filename):
    directory = 'trollApp/trollCode/downloads/'
    wrapper = FileWrapper(open(directory + filename, 'rb'))
    content_type = guess_type(filename)[0]
    
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
    CREATE_NO_WINDOW = 0x08000000
    returnCode = call("python {}/convertToExe.py -f {}"
                      .format(codeDirectory, tmpFile),
                      creationflags = CREATE_NO_WINDOW)

    if returnCode != 0: # fail
        return HttpResponse("Sorry! It looks like we couldn't convert your code. Please try submitting again.")
        
    exeFilename = tmpFile.replace(".py", ".exe")
    exeDirectory = 'trollApp/customTrollCode/downloads/'
    wrapper = FileWrapper(open(exeDirectory + exeFilename, 'rb'))
    content_type = guess_type(exeFilename)[0]

    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(exeFilename)
    return response

def displaySuggestions(request):
    return render(request, 'trollApp/suggestionsDisplay.html')

# TODO: Get email server for this method to work!
def sendSuggestion(request):
    emailBody = request.POST.get("suggestion", "")
##    send_mail("Troll Suggestion", emailBody, "no-reply@trollMaster.com",
##              ['duhtrollmaster@gmail.com'], fail_silently = False)
    return HttpResponse("The troll master thanks you for the email.")
