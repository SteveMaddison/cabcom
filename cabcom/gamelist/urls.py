from django.conf.urls import patterns, url
from cabcom.gamelist import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<object_type>\w+)/$', views.index, name='index'),
	url(r'^(?P<object_type>\w+)/(?P<game_id>\d+)/$', views.detail, name='detail'),
)