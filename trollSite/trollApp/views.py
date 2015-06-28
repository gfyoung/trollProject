from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'trollApp/download.html')

def downloadTest(request):
    filename = 'trollApp/downloads/test.txt'
    wrapper = FileWrapper(open(filename))
    content_type = 'text/plain'
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="sucess.txt"'
    return response
    
