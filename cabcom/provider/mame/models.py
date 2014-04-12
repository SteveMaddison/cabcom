from django.db import models
from cabcom.provider.models import Provider, ProviderException
from cabcom.gamelist.models import Game, Data, Genre, Publisher, Platform, ControlType
from xml.etree.ElementTree import iterparse
import os
import subprocess
from datetime import datetime

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
		added = 0

		if self.resource_type != 'g' and self.resource_type != 'd':
			raise ProviderException('Provider does not support resource type.')

		if self.xml_file:
			if not os.path.exists(self.xml_file):
				if not self.executable:
					raise ProviderException('Executable not set.')

				if not os.path.exists(self.executable):
					raise ProviderException('No such file or directory.')

				# Run MAME to get the game list XML.
				f = open(self.xml_file, 'w')
				f.write(subprocess.check_output([self.executable, '-listxml']))
				f.close

		# As the data can always be restored by re-running the import,
		# it's easiest just to throw all records away and start again.
		self.clear()

		context = iterparse(self.xml_file, events=('start', 'end'))
		context = iter(context)
		event, root = context.next()

		for event, element in context:
			if event == 'end' and element.tag == 'game':
				description = element.find('description').text
				manufacturer = element.find('manufacturer').text

				if manufacturer:
					publisher, created = Publisher.objects.get_or_create(name = manufacturer)

				if self.resource_type == 'g':
					item = Game(
						name = element.get('name'),
						display_name = description,
						publisher = publisher,
						platform = self.platform,
						provider = self,
					)
				elif self.resource_type == 'd':
					item = Data(
						name = element.get('name'),
						display_name = description,
						publisher = publisher,
						platform = self.platform,
						provider = self,
					)

				year = element.find('year').text
				try:
					int(year)
					release_date = datetime.strptime('01-01-' + year, '%d-%m-%Y').date()
					item.release_date = release_date
				except:
					pass				

				item.save()

				for control in element.find('input').findall('control'):
					control_type_name = control.get('type')
					control_type, created = ControlType.objects.get_or_create(name = control_type_name)
					item.control_types.add(control_type)

				root.clear()
				added += 1

				if added == 10:
					return added

		return added

