from django.http import Http404
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from cabcom.frontend.cabrio.models import Cabrio
import os

class CabrioView(DetailView):
	model = Cabrio
	template_name = 'frontend/cabrio/detail.html'

	def get_object(self):
		object, created = Cabrio.objects.get_or_create()

		if created:
			object.name = 'Cabrio'
			object.save()

		return object

