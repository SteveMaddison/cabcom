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
		object, created = Mame.objects.get_or_create()

		if created:
			object.name = 'MAME'
			object.resource_type = 'd'
			object.executable = self.find_mame_executable()
			object.save()

		return object

	def post(self, request, *args, **kwargs):
		mame = self.get_object()

		if mame.idle:
			if 'executable' in self.request.POST:
				executable = self.request.POST['executable']
				if executable:
					mame.executable = executable
				else:
					mame.executable = self.find_mame_executable()

			if 'platform_name' in self.request.POST:
				platform_name = self.request.POST['platform_name']
				if platform_name:
					platform, created = Platform.objects.get_or_create(name = platform_name)
					mame.platform = platform

			mame.inventory = 0
			mame.imported = 0
			mame.save()
			mame.refresh()

		return self.get(self, request, *args, **kwargs)

	def get_context_data(self, **kwargs):
		mame = self.get_object()

		context = super(MameView, self).get_context_data(**kwargs)
		context['title'] = 'MAME'
		context['menu_active'] = 'data'
		context['platforms'] = Platform.objects.all().order_by('name')

		if mame.inventory > 0:
			context['imported_percent'] = int(float(mame.imported) / float(mame.inventory) * 100)

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

