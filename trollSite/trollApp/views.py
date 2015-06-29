from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render
from mimetypes import guess_type

# TODO: Consider making a Model class if the number of examples become massive
class Download(object):
    def __init__(self, filename, description):
        self.filename = filename
        self.description = description

    def __unicode__(self):
        return "{}: {}".format(self.filename, self.description)
    
def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')

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
    directory = 'trollApp/downloads/'
    wrapper = FileWrapper(open(directory + filename, 'rb'))
    content_type = guess_type(filename)[0]
    
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    return response
    
