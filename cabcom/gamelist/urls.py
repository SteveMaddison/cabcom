from django.conf.urls import patterns, url
from cabcom.gamelist.views import IndexView, GameListView, DataListView, GameDetailView, DataDetailView, GameImportView, GamePopulateView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^data/$', DataListView.as_view(), name='data'),
	url(r'^data/(?P<pk>\d+)/$', DataDetailView.as_view(), name='data-detail'),
	url(r'^game/$', GameListView.as_view(), name='game'),
	url(r'^game/(?P<pk>\d+)/$', GameDetailView.as_view(), name='game-detail'),
	url(r'^import/$', GameImportView.as_view(), name='import'),
	url(r'^populate/$', GamePopulateView.as_view(), name='populate'),
)
