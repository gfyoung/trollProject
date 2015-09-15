from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView
from django.contrib import admin


def getAdminRoot():
    import django
    from os.path import dirname
    return dirname(django.__file__) + "/contrib/admin/static/admin"

# We abstract the 'adminRoot' creation
# into a method for clarity purposes
adminRoot = getAdminRoot()

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(url='/trollApp/', permanent=False)),
    url(r'^trollApp$', RedirectView.as_view(
        url='/trollApp/', permanent=False)),
    url(r'^trollApp/', include('trollApp.urls', namespace='trollApp')),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/admin/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': adminRoot}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': 'trollApp/static'}),
    url(r'^.*$', 'django.views.defaults.page_not_found')
)
