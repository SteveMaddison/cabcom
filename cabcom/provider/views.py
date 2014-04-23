from django.http import Http404, HttpRequest
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from cabcom.provider.directory.models import Directory


class IndexView(RedirectView):
	permanent = False
	query_string = True

	def get_redirect_url(self):
		return reverse_lazy('provider:title')

class MediaIndexView(ListView):
	template_name = 'provider/index.html'
	context_object_name = 'providers'
	resource_type = None

	def get_queryset(self):
		return Directory.objects.filter(resource_type = self.resource_type).order_by('name')

	def get_context_data(self, **kwargs):
		context = super(MediaIndexView, self).get_context_data(**kwargs)
		context['menu_active'] = 'media'

		if self.resource_type == 'b':
			context['title'] = 'Backgrounds'
		elif self.resource_type == 's':
			context['title'] = 'Screenshots'
		elif self.resource_type == 't':
			context['title'] = 'Titles'
		elif self.resource_type == 'v':
			context['title'] = 'Videos'
		else:
			raise Exception('Unsupported media resource type.')

		return context

	def post(self, request, *args, **kwargs):
		if 'id' in self.request.POST:
			provider_id = self.request.POST['id']

		if 'delete' in self.request.POST:
			# Delete the selected provider.
			if provider_id:
				provider = Directory.objects.get(id = provider_id)
				provider.delete()

		elif 'add' in self.request.POST:
			# Adding new
			provider = Directory(resource_type = self.resource_type)

			if 'name' in self.request.POST:
				name = self.request.POST['name']
				if name:
					provider.name = name

			if 'path' in self.request.POST:
				path = self.request.POST['path']
				if path:
					provider.path = path

			provider.save()

		return self.get(self, request, *args, **kwargs)

class BackgroundIndexView(MediaIndexView):
	resource_type = 'b'

class ScreenshotIndexView(MediaIndexView):
	resource_type = 's'

class TitleIndexView(MediaIndexView):
	resource_type = 't'

class VideoIndexView(MediaIndexView):
	resource_type = 'v'
