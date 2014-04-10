from django.db import models
from cabcom.gamelist.models import Game

class Provider(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

	def games(self):
		return Game.objects.filter(provider = self)

	def clear(self):
		self.games.delete()

	def refresh(self):
		try:
			for f in self.list():
				if self.games().filter(name = f).count() == 0:
					g = Game(name = f, provider = self)
					g.save()

		except AttributeError:
			# No "list" method, OK.
			pass

class ProviderException(Exception):
	def __init__(self, value):
		self.value = value

	def __unicode__(self):
		return repr(self.value)

