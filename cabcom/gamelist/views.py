from django.http import Http404
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404
from cabcom.gamelist.models import Game, Data

class IndexView(RedirectView):
	permanent = True
	query_string = True

	def get_redirect_url(self):
		return reverse('game')

class GameListView(ListView):
	model = Game
	template_name = 'gamelist/index.html'
	context_object_name = 'games'
	paginate_by = 50

	def get_context_data(self, **kwargs):
		context = super(GameListView, self).get_context_data(**kwargs)
		context['title'] = 'Game List'
		context['detail_type'] = 'game'
		context['menu_active'] = 'game'
		return context

class DataListView(GameListView):
	model = Data

	def get_context_data(self, **kwargs):
		context = super(DataListView, self).get_context_data(**kwargs)
		context['title'] = 'Game Database'
		context['detail_type'] = 'data'
		context['menu_active'] = 'data'
		return context

class GameDetailView(DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'gamelist/detail.html'

	def get_context_data(self, **kwargs):
		context = super(GameDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Game List'
		context['menu_active'] = 'game'
		return context

class DataDetailView(GameDetailView):
	model = Data

	def get_context_data(self, **kwargs):
		context = super(DataDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Game Database'
		context['menu_active'] = 'data'
		return context
