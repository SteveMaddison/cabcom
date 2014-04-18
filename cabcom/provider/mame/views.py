from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404
from cabcom.provider.mame.models import Mame

class MameView(DetailView):
	model = Mame
	template_name = 'provider/mame/detail.html'

	def get_object(self):
		object, created = Mame.objects.get_or_create(id=1)
		return object

	def get_context_data(self, **kwargs):
		context = super(MameView, self).get_context_data(**kwargs)
		context['title'] = 'MAME'
		context['menu_active'] = 'data'
		return context
