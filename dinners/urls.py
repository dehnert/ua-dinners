from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout
from django.views.generic.list_detail import object_list, object_detail

import dinners.core.views
import dinners.core.models
import people.views

import settings

urlpatterns = patterns('',
    # Example:
    # (r'^dinners/', include('dinners.foo.urls')),
    url(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html', 'extra_context': { 'pagename':'homepage' }, }, name='homepage'),
    url(r'^dinners/$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html', 'extra_context': { 'pagename':'homepage' }, }, name='homepage'),
    url(r'^search/$', people.views.search_person, name='search', ),
    url(r'^view/$', dinners.core.views.select_program, {'forview':'view_dinners'}, 'view_dinners'),
    url(r'^view/(?P<program_slug>[a-z0-9-]+)/$', dinners.core.views.view_dinners, name='view_dinners', ),
    url(r'^view/(?P<program_slug>[a-z0-9-]+)/(?P<dinner_id>[0-9]+)$', dinners.core.views.view_dinner, name='view_dinner', ),
    url(r'^register/$', dinners.core.views.select_program, {'forview':'register_dinner'}, 'register_dinner'),
    url(r'^register/(?P<program_slug>[a-z0-9-]+)/$', dinners.core.views.register_dinner, name='register_dinner', ),
    url(r'^(?P<action>confirm|reject)/(?P<dinner_id>[0-9]+)$', dinners.core.views.confirm_dinner, name='confirm_dinner', ),
    url(r'^schedule/(?P<dinner_id>[0-9]+)$', dinners.core.views.schedule_dinner, name='schedule_dinner', ),

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
