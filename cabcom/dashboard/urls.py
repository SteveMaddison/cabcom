from django.conf.urls import patterns, url
from cabcom.dashboard import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index')
)
