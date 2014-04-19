from django.db import models
from cabcom.provider.models import Provider, ProviderException
from cabcom.gamelist.models import Game, Data, Genre, Publisher, Platform, ControlType
from cabcom.provider.mame.tasks import import_xml

class Mame(Provider):
	executable = models.CharField(max_length = 256)
	xml_file = models.CharField(max_length = 256, default = 'mame.xml')
	platform = models.ForeignKey(Platform, blank = True, null = True)

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
		# As we may have many thousands of records, a regular .delete()
		# doesn't always work, so we do it the hard way.
		for item in self.items():
			item.delete()

	def refresh(self):
		if self.resource_type != 'g' and self.resource_type != 'd':
			raise ProviderException('Provider does not support resource type.')

		import_xml.delay(self)

		return 0
