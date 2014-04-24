from django.http import Http404
from django.forms import ModelForm
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from cabcom.frontend.cabrio.models import Cabrio
import os

class CabrioForm(ModelForm):
	class Meta:
		model = Cabrio
		fields = [
			'config_dir',
			'fullscreen',
			'framerate',
			'theme',
			'screen_width',
			'screen_height',
			'rotation',
			'gfx_quality',
			'max_image_width',
			'max_image_height',
		]

class CabrioView(View):
	template_name = 'frontend/cabrio/detail.html'

	def get_object(self):
		object, created = Cabrio.objects.get_or_create()

		if created:
			object.name = 'Cabrio'
			object.save()

		return object

	def get(self, request, *args, **kwargs):
		cabrio = self.get_object()

		form = CabrioForm(instance = cabrio)

		return render(request, self.template_name, { 'form': form })

	def post(self, request, *args, **kwargs):
		cabrio = self.get_object()

		form = CabrioForm(request.POST, instance = cabrio)
		if form.is_valid():
			form.save()

		return render(request, self.template_name, { 'form': form })

