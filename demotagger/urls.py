from django.conf.urls.defaults import patterns, include, url
from media_wkf import views as mw_views
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', mw_views.index, name='mw_index'),
    url(r'^media_wkf/', include('demotagger.media_wkf.urls')),
    # url(r'^demotagger/', include('demotagger.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,})
)
