from django.conf.urls import patterns, url
from cabcom.gamelist import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)
