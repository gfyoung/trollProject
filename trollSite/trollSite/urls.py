from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib.auth import views as authViews
from django.views.generic.base import RedirectView
from trollApp.admin import adminSite


def getAdminRoot():
    import django
    from os.path import dirname
    return dirname(django.__file__) + "/contrib/admin/static/admin"

# We abstract the 'adminRoot' creation
# into a method for clarity purposes
adminRoot = getAdminRoot()

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/trollApp/', permanent=False)),
    url(r'^trollApp$', RedirectView.as_view(
        url='/trollApp/', permanent=False)),
    url(r'^trollApp/', include('trollApp.urls', namespace='trollApp')),
    url(r'^admin$', RedirectView.as_view(url='/admin/', permanent=False)),
    url(r'^admin/', include(adminSite.urls)),
    url(r'^admin/password_reset/$', authViews.password_reset,
        {'template_name': 'trollSiteAdmin/passwordResetForm.html'},
        name='admin_password_reset'),
    url(r'^admin/password_reset/done/$', authViews.password_reset_done,
        {'template_name': 'trollSiteAdmin/passwordResetDone.html'},
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        authViews.password_reset_confirm,
        {'template_name': 'trollSiteAdmin/passwordResetConfirm.html'},
        name='password_reset_confirm'),
    url(r'^reset/done/$', authViews.password_reset_complete,
        {'template_name': 'trollSiteAdmin/passwordResetComplete.html'},
        name='password_reset_complete'),
] + static(r'^static/admin/(?P<path>.*)$', document_root=adminRoot) \
  + static(r'^static/(?P<path>.*)$', document_root='trollApp/static')
