from django.conf.urls import patterns, url
from cabcom.provider.mame.views import MameView

urlpatterns = patterns('',
	url(r'^mame/$', MameView.as_view(), name='mame'),
)
