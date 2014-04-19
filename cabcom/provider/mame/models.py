from django.db import models
from django.db import connection
from cabcom.provider.models import Provider, ProviderException
from cabcom.gamelist.models import Game, Data, Genre, Publisher, Platform, ControlType
from cabcom.provider.mame.tasks import import_xml

class Mame(Provider):
	executable = models.CharField(max_length = 256)
	platform = models.ForeignKey(Platform, blank = True, null = True)
	idle = models.BooleanField(default = True)
	inventory = models.IntegerField(default = 0)
	imported = models.IntegerField(default = 0)

	class Meta:
		verbose_name = 'MAME Provider'

	def __unicode__(self):
		return self.name

	def items(self):
		if self.resource_type == 'g':
			return Game.objects.filter(provider = self)
		elif self.resource_type == 'd':
			return Data.objects.filter(provider = self)
		else:
			raise ProviderException('Provider does not support resource type.')

	def clear(self):
		if self.resource_type != 'g' and self.resource_type != 'd':
			raise ProviderException('Provider does not support resource type.')

		# Deleting with a filter can result in errors when too many records
		# are involved, so we do it by hand.
		cursor = connection.cursor()
		if self.resource_type == 'g':
			cursor.execute('DELETE from gamelist_game WHERE provider_id = %s', [self.id])
		elif self.resource_type == 'd':
			cursor.execute('DELETE from gamelist_data WHERE provider_id = %s', [self.id])

		# Reset out counters.
		self.inventory = 0
		self.imported = 0
		self.save()

	def refresh(self):
		if self.resource_type != 'g' and self.resource_type != 'd':
			raise ProviderException('Provider does not support resource type.')

		self.idle = False
		self.save()

		import_xml.delay(self)

		return 0
