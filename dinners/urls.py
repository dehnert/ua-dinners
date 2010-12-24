from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout

import settings

urlpatterns = patterns('',
    # Example:
    # (r'^dinners/', include('dinners.foo.urls')),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html', 'extra_context': { 'pagename':'homepage' }, }, 'homepage'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/',  login,  name='login', ),
    url(r'^accounts/logout/', logout, name='logout', ),
)

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del(_media_url, serve)
