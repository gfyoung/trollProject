from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin

import django.views.defaults

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/trollApp/', permanent=False)),
    url(r'^trollApp/', include('trollApp.urls', namespace='trollApp')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'trollApp/static'}
    ),
    url(r'^.*$', 'django.views.defaults.page_not_found')
)
