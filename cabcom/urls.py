from django.conf.urls import patterns, include, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', include('cabcom.dashboard.urls', namespace='dashboard')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^gamelist/', include('cabcom.gamelist.urls', namespace='gamelist')),
	url(r'^login/', include('cabcom.login.urls', namespace='login')),
)
