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

		# Set up an interative XML parser so we can discard processed
		# items when we're done.
		context = iterparse(self.xml_file, events=('start', 'end'))
		context = iter(context)
		event, root = context.next()

		for event, element in context:
			if event == 'end' and element.tag == 'game':
				manufacturer = element.find('manufacturer')
				if manufacturer != None:
					publisher, created = Publisher.objects.get_or_create(name = manufacturer.text)
				else:
					publisher = None

				if self.resource_type == 'g':
					item = Game(
						name = element.get('name'),
						publisher = publisher,
						platform = self.platform,
						provider = self,
					)
				elif self.resource_type == 'd':
					item = Data(
						name = element.get('name'),
						publisher = publisher,
						platform = self.platform,
						provider = self,
					)

				description = element.find('description')
				if description != None:
					item.display_name = description.text

				year = element.find('year')
				if year != None:
					try:
						int(year.text)
						# We only know the year, so just fill in 1st January.
						release_date = datetime.strptime('01-01-' + year.text, '%d-%m-%Y').date()
						item.release_date = release_date
					except:
						pass				

				item.save()

				input_element = element.find('input')
				if input_element != None:
					controls = input_element.findall('control')
					if controls != None:
						for control in controls:
							control_type_name = control.get('type')
							control_type, created = ControlType.objects.get_or_create(name = control_type_name)
							item.control_types.add(control_type)

				root.clear()
				added += 1

		return added


