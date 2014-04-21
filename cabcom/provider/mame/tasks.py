from __future__ import absolute_import
from celery import shared_task
import os
from tempfile import mkstemp
import subprocess
from datetime import datetime
from xml.etree.ElementTree import iterparse
from cabcom.gamelist.models import Game, Data, Genre, Publisher, Platform, ControlType

@shared_task()
def import_xml(self):
	added = 0

	if not self:
		raise ProviderException('No MAME provider configured')

	if not self.executable:
		raise ProviderException('Executable not set.')

	if not os.path.exists(self.executable):
		raise ProviderException('No such file or directory.')

	# Run MAME to get the game list XML into a temporary file.
	f, xml_file = mkstemp()
	os.write(f, subprocess.check_output([self.executable, '-listxml']))
	os.close(f)

	# As the data can always be restored by re-running the import,
	# it's easiest just to throw all records away and start again.
	self.clear()

	# Set up an interative XML parser so we can discard processed
	# items when we're going.
	context = iterparse(xml_file, events=('start', 'end'))
	context = iter(context)
	event, root = context.next()

	# First, count the items without processing, so we can follow
	# progress later.
	for event, element in context:
		if event == 'end' and element.tag == 'game':
			self.inventory += 1
			if self.inventory % 100 == 0:
				self.save()
			root.clear()
	# Save the exact number.
	self.save()

	# This time really import the games.
	context = iterparse(xml_file, events=('start', 'end'))
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

			# Update the running total, but not too often.
			if added % 100 == 0:
				self.imported = added
				self.save()

	# Updte with the exact number imported.
	self.imported = added
	self.idle = True
	self.save()

	os.unlink(xml_file)

	return added
