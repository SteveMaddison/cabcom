from django.conf.urls import patterns, url
from cabcom.frontend.cabrio.views import CabrioView

urlpatterns = patterns('',
	url(r'^cabrio/$', CabrioView.as_view(), name='cabrio'),
)
