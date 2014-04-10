from django.db import models
from cabcom.gamelist.models import Game
from os.path import splitext

RESOURCE_TYPES = (
	('g', 'Games'),
	('i', 'Images'),
	('i', 'Videos'),
)

class Provider(models.Model):
	name = models.CharField(max_length=50, unique=True)
	resource_type = models.CharField(max_length=1, choices=RESOURCE_TYPES)

	def __unicode__(self):
		return self.name

	def games(self):
		return Game.objects.filter(provider = self)

	def clear(self):
		self.games.delete()

	def refresh(self):
		if self.resource_type == 'g':
			try:
				for f in self.list():
					if self.games().filter(name = f).count() == 0:
						g = Game(
							name = f,
							provider = self,
							display_name = splitext(f)[0].title()
						)
						g.save()

			except AttributeError:
				# No "list" method, OK.
				pass
		elif self.resource_type == 'i':
			# nothing yet
			return
		elif self.resource_type == 'v':
			# nothing yet
			return
		else:
			raise ProviderException('No such resource type.')

class ProviderException(Exception):
	def __init__(self, value):
		self.value = value

	def __unicode__(self):
		return repr(self.value)

