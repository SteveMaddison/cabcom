from django.conf.urls import patterns, url
from cabcom.provider.views import BackgroundIndexView, ScreenshotIndexView, TitleIndexView, VideoIndexView
from cabcom.provider.mame.views import MameView

urlpatterns = patterns('',
	url(r'^mame/$', MameView.as_view(), name='mame'),
	url(r'^background/$', BackgroundIndexView.as_view(), name='background'),
	url(r'^screenshot/$', ScreenshotIndexView.as_view(), name='screenshot'),
	url(r'^title/$', TitleIndexView.as_view(), name='title'),
	url(r'^video/$', VideoIndexView.as_view(), name='video'),
)
