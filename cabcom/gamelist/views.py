from django.http import Http404, HttpRequest
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404
from cabcom.gamelist.models import Game, Data, Platform
from cabcom.provider.directory.models import Directory

class IndexView(RedirectView):
	permanent = False
	query_string = True

	def get_redirect_url(self):
		return reverse_lazy('gamelist:game')

class GameListView(ListView):
	template_name = 'gamelist/index.html'
	context_object_name = 'games'
	ordering = ['-display_name']
	paginate_by = 50

	def get_queryset(self):
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			if q:
				return Game.objects.filter(display_name__icontains = q).order_by('display_name')

		return Game.objects.order_by('display_name')

	def get_context_data(self, **kwargs):
		context = super(GameListView, self).get_context_data(**kwargs)
		context['title'] = 'Game List'
		context['detail_type'] = 'game'
		context['menu_active'] = 'game'

		if 'q' in self.request.GET:
			context['search'] = self.request.GET['q']

		return context

class DataListView(GameListView):
	def get_queryset(self):
		if 'q' in self.request.GET:
			q = self.request.GET['q']
			if q:
				return Data.objects.filter(display_name__icontains = q).order_by('display_name')

		return Data.objects.order_by('display_name')

	def get_context_data(self, **kwargs):
		context = super(DataListView, self).get_context_data(**kwargs)
		context['title'] = 'Game Database'
		context['detail_type'] = 'data'
		context['menu_active'] = 'data'

		if 'q' in self.request.GET:
			context['search'] = self.request.GET['q']

		return context

class GameDetailView(DetailView):
	model = Game
	context_object_name = 'game'
	template_name = 'gamelist/detail.html'

	def get_media(self, provider):
		if provider:
			dir = Directory.objects.get(id = provider.id)
			if dir:
				files = dir.match(self.object.name)
				if files:
					return files[0]

		return None

	def get_context_data(self, **kwargs):
		context = super(GameDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Game List'
		context['detail_type'] = 'game'
		context['menu_active'] = 'game'
		context['title_file']      = self.get_media(self.object.title_provider)
		context['screenshot_file'] = self.get_media(self.object.screenshot_provider)
		context['background_file'] = self.get_media(self.object.background_provider)
		context['video_file']      = self.get_media(self.object.video_provider)

		return context

class DataDetailView(GameDetailView):
	model = Data

	def get_context_data(self, **kwargs):
		context = super(DataDetailView, self).get_context_data(**kwargs)
		context['title'] = 'Game Database'
		context['detail_type'] = 'data'
		context['menu_active'] = 'data'
		return context

class GameImportView(ListView):
	template_name = 'gamelist/import.html'
	context_object_name = 'dirs'

	def get_queryset(self):
		return Directory.objects.filter(resource_type = 'g').order_by('name')

	def get_context_data(self, **kwargs):
		context = super(GameImportView, self).get_context_data(**kwargs)
		context['menu_active'] = 'game'
		context['platforms'] = Platform.objects.all().order_by('name')

		return context

	def post(self, request, *args, **kwargs):
		if 'id' in self.request.POST:
			provider_id = self.request.POST['id']

		if 'delete' in self.request.POST:
			# Delete the selected provider.
			if provider_id:
				provider = Directory.objects.get(id = provider_id)
				provider.delete()
			
		elif 'refresh' in self.request.POST:
			# Refresh the provider
			if id:
				provider = Directory.objects.get(id = provider_id)
				provider.refresh()

		elif 'add' in self.request.POST:
			# Adding new
			provider = Directory(resource_type = 'g')

			if 'name' in self.request.POST:
				name = self.request.POST['name']
				if name:
					provider.name = name

			if 'path' in self.request.POST:
				path = self.request.POST['path']
				if path:
					provider.path = path

			provider.save()
			provider.refresh()

			if 'platform_name' in self.request.POST:
				platform_name = self.request.POST['platform_name']
				if platform_name:
					platform, created = Platform.objects.get_or_create(name = platform_name)
					Game.objects.filter(provider = provider).update(platform = platform)

		return self.get(self, request, *args, **kwargs)

class GamePopulateView(RedirectView):
	permanent = False
	query_string = True

	def get_redirect_url(self):
		for game in Game.objects.all():
			game.populate()

			# TODO: fix this and abstract for different provider types
			if not game.title_provider:
				for title_provider in Directory.objects.filter(resource_type = 't'):
					if title_provider.match(game.name):
						game.title_provider = title_provider
						game.save()

			if not game.screenshot_provider:
				for screenshot_provider in Directory.objects.filter(resource_type = 's'):
					if screenshot_provider.match(game.name):
						game.screenshot_provider = screenshot_provider
						game.save()

			if not game.background_provider:
				for background_provider in Directory.objects.filter(resource_type = 'b'):
					if background_provider.match(game.name):
						game.background_provider = background_provider
						game.save()

			if not game.video_provider:
				for video_provider in Directory.objects.filter(resource_type = 'v'):
					if video_provider.match(game.name):
						game.video_provider = video_provider
						game.save()

		return reverse_lazy('gamelist:game')

