from django.conf.urls.defaults import patterns, include, url
from media_wkf import views as mw_views

urlpatterns = patterns('',
    url(r'^add_comment/$', mw_views.add_comment, name='add_comment'),
)