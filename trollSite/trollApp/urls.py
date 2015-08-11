from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
from trollApp import views

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url = '/trollApp/home', permanent = False)),
    url(r'^home$', views.displayWelcome, name = 'home'),
    url(r'^about$', views.displayAbout, name = 'about'),
    url(r'^downloads$', views.displayDownloads, name = 'downloads'),
    url(r'^downloads/(?P<os>\w+)/(?P<filename>\w+.\w+)$', views.downloadFile, name = 'downloadFile'),
    url(r'^customCreation$', views.displayCustomCreate, name = 'customCreate'),
    url(r'^customCreation/download$', views.downloadCustomFile, name = 'customDownload'),
    url(r'^suggestions$', views.displaySuggestions, name = 'suggestions'),
    url(r'^sendSuggestion$', views.sendSuggestion, name = 'sendSuggestion'),
    url(r'^playTrollSong$', views.playTrollSong, name = 'playTrollSong'),
    url(r'^trollifyEmail$', views.displayTrollifyEmail, name = 'displayTrollEmail'),
    url(r'^trollifyEmail/create$', views.trollifyEmail, name = 'trollEmail')
)
