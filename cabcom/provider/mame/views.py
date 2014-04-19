from django.http import Http404
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from cabcom.provider.mame.models import Mame
from cabcom.gamelist.models import Platform
import os

class MameView(DetailView):
	model = Mame
	template_name = 'provider/mame/detail.html'

	def get_object(self):
		object, created = Mame.objects.get_or_create(id=1)

		if created:
			object.name = 'MAME'
			object.resource_type = 'd'
			object.executable = self.find_mame_executable()
			object.save()

		return object

	def post(self, request, *args, **kwargs):
		mame = self.get_object()

		if 'executable' in self.request.POST:
			executable = self.request.POST['executable']
			if executable:
				mame.executable = executable
			else:
				mame.executable = self.find_mame_executable()

		if 'platform' in self.request.POST:
			platform = Platform.objects.get(id = self.request.POST['platform'])
			if platform:
				mame.platform = platform

		mame.save()
		mame.refresh()

		return self.get(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		context = super(MameView, self).get_context_data(**kwargs)
		context['title'] = 'MAME'
		context['menu_active'] = 'data'
		context['platforms'] = Platform.objects.all().order_by('name')
		return context

	def find_mame_executable(self):
		# Try to find the mame executable in the path.
		env_path = os.environ.get('PATH')
		if env_path:
			for directory in env_path.split(':'):
				attempt = os.path.join(directory,'mame')
				if os.path.exists(attempt):
					return attempt

		return None

