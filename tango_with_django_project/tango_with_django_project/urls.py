from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^myrango/', include('myrango.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('myrango.urls')),
    url(r'^rango/test/$',include('rangotest.urls')), # ADD THIS NEW TUPLE!
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.views.static',
        (r'media/(?P<path>.*)',
        'serve',
        {'document_root': settings.MEDIA_ROOT}), )
