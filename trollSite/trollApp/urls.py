from django.conf.urls import patterns, url
from trollApp import views

urlpatterns = patterns('',
    url(r'^$', views.displayWelcome, name = 'home'),
    url(r'^downloads$', views.displayDownloads, name = 'downloads'),
    url(r'^downloads/(?P<filename>\w+.\w+)$', views.downloadFile, name = 'downloadFile'),
    url(r'^customCreation$', views.displayCustomCreate, name = 'customCreate')
)
