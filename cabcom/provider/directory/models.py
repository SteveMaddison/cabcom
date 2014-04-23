from django.db import models
from cabcom.provider.models import Provider, ProviderException
from cabcom.gamelist.models import Game
from os.path import splitext
import os

class Directory(Provider):
	path = models.CharField(max_length=256)

	class Meta:
		verbose_name = 'Directory Provider'

	def __unicode__(self):
		return self.name

	def check(self):
		if not self.path:
			raise ProviderException('Path not set.')

		if not os.path.exists(self.path):
			raise ProviderException('No such file or directory.')

		if not os.path.isdir(self.path):
			raise ProviderException('Not a directory.')

	def list(self):
		return os.listdir(self.path)

	def match(self, name, extension = ''):
		self.check()

		if not name:
			raise ProviderException('No name provided.')

		pattern = name + '.' + extension
		results = []

		if extension:
			self.check()
			match = os.path.join(self.path, pattern)
			if os.path.isfile(match):
				results.append(match)
		else:
			for f in self.list():
				if f.startswith(pattern):
					results.append(os.path.join(self.path,f))

		return results

	def refresh(self):
		added = 0

		if self.resource_type == 'g':
			games = Game.objects.filter(provider = self)

			for f in self.list():
				if games.filter(file_name = f).count() == 0:
					g = Game(
						name = splitext(f)[0],
						file_name = f,
						provider = self,
						display_name = splitext(f)[0].title(),
					)
					g.save()
					added += 1
		elif self.resource_type == 'i':
			# nothing yet
			return 0
		elif self.resource_type == 'v':
			# nothing yet
			return 0
		elif self.resource_type == 'd':
			# nothing yet
			return 0
		else:
			raise ProviderException('No such resource type.')

		return added

