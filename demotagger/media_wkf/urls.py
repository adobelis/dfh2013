from django.conf.urls.defaults import patterns, include, url
from media_wkf import views as mw_views

urlpatterns = patterns('',
    url(r'^login_user', mw_views.login_user, name='login_user'),
    url(r'^add_comment/$', mw_views.add_comment, name='add_comment'),
    url(r'^sample_presentation/(?P<workspace_index>\d+)/(?P<preso_index>\d+)/$', mw_views.sample_preso, name='sample_preso'),
    url(r'^media_item/(?P<workspace_index>\d+)/(?P<mi_index>\d+)/$', mw_views.media_item, name='media_item'),
)