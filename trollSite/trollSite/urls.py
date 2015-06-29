from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url = '/trollApp/', permanent = False)),
    url(r'^trollApp/', include('trollApp.urls', namespace = 'trollApp')),
    url(r'^admin/', include(admin.site.urls))
)
