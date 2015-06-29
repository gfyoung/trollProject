from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render

def displayWelcome(request):
    return render(request, 'trollApp/welcomeDisplay.html')

def displayDownloads(request):
    return render(request, 'trollApp/downloadsDisplay.html')

def downloadTest(request):
    filename = 'trollApp/downloads/test.txt'
    wrapper = FileWrapper(open(filename))
    content_type = 'text/plain'
    response = HttpResponse(wrapper, content_type = content_type)
    response['Content-Disposition'] = 'attachment; filename="success.txt"'
    return response
    
