from django.db import models
from cabcom.frontend.models import FrontEnd, FrontEndException
from cabcom.gamelist.models import Game, Filter
from cabcom.provider.models import Provider
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os
import re

EVENT_TYPES = (
	('u', 'Up'),
	('d', 'Down'),
	('l', 'Left'),
	('r', 'Right'),
	('s', 'Select'),
	('b', 'Back'),
	('q', 'Quit'),
)

DEVICE_TYPES = (
	('j', 'Joystick'),
	('k', 'Keyboard'),
	('m', 'Mouse'),
)

CONTROL_TYPES = (
	('a', 'Axis'),
	('b', 'Button'),
	('h', 'Hat'),
	('t', 'Ball'),
)

ROTATION_VALUES = (
	(0,   0),
	(90,  90),
	(180, 180),
	(270, 270),
)

GFX_VALUES = (
	('l', 'Low'),
	('m', 'Medium'),
	('h', 'High'),
)

LOCATION_TYPES = (
	('b', 'Background'),
	('l', 'Logo'),
	('s', 'Screenshot'),
	('v', 'Video'),
)

class Control(models.Model):
	event = models.CharField(max_length = 1, choices = EVENT_TYPES, unique = True)
	device_type = models.CharField(max_length = 1, choices = DEVICE_TYPES)
	device_id = models.IntegerField(default = 0)
	control_type = models.CharField(max_length = 1, choices = CONTROL_TYPES)
	control_id = models.IntegerField(default = 0)
	value = models.CharField(max_length = 10)

	class Meta:
		verbose_name = 'Cabrio Control'

	def __unicode__(self):
		return self.get_event_display()

class Theme(models.Model):
	name = models.CharField(max_length = 50)

	class Meta:
		verbose_name = 'Cabrio Theme'

	def __unicode__(self):
		return self.name

class GameList(models.Model):
	name = models.CharField(max_length = 50)
	filter = models.ForeignKey(Filter, blank = True, null = True)

	class Meta:
		verbose_name = 'Cabrio Game List'

	def __unicode__(self):
		return self.name

	def file_name(self):
		file_name = self.name

		non_alphanum = re.compile('[\s \W]+')
		file_name = non_alphanum.sub('_', file_name)

		normalise = re.compile('_+')
		file_name = normalise.sub('_', file_name)

		return file_name.lower() + '.xml'

	def games(self):
		if self.filter:
			return self.filter.games()
		else:
			return Game.objects.all()

	def config(self):
		root = ET.Element('cabrio-config')

		# General
		game_list = ET.SubElement(root, 'game-list')
		name = ET.SubElement(game_list, 'name')
		name.text = str(self.name)
		games = ET.SubElement(game_list, 'games')

		# Game entries
		total = 0
		for g in self.games():
			game = ET.SubElement(games, 'game')
			name = ET.SubElement(game, 'name')
			name.text = str(g.name)
			total += 1

		print total

		return ET.tostring(root)

class Location(models.Model):
	type = models.CharField(max_length = 1, choices = LOCATION_TYPES)
	provider = models.ForeignKey(Provider)

	class Meta:
		verbose_name = 'Cabrio Location'

	def __unicode__(self):
		return str(self.get_type_display())

class Cabrio(FrontEnd):
	config_dir = models.CharField(max_length = 256)

	# General config
	fullscreen = models.BooleanField(default = True)
	framerate = models.IntegerField(default = 60)
	theme = models.ForeignKey(Theme, blank=True, null=True)

	# Screen config
	screen_width = models.IntegerField(default = 800)
	screen_height = models.IntegerField(default = 600)
	rotation = models.IntegerField(default = 0, choices = ROTATION_VALUES)

	# Graphics config
	gfx_quality = models.CharField(max_length = 1, default = 'h', choices = GFX_VALUES)
	max_image_width = models.IntegerField(default = 512)
	max_image_height = models.IntegerField(default = 512)

	class Meta:
		verbose_name = 'Cabrio Front End'

	def __unicode__(self):
		return 'Cabrio'

	def config(self):
		root = ET.Element('cabrio-config')

		# Interface / General
		interface = ET.SubElement(root, 'interface')
		fullscreen = ET.SubElement(interface, 'full-screen')
		fullscreen.text = str(self.fullscreen).lower()
		framerate = ET.SubElement(interface, 'framerate')
		framerate.text = str(self.framerate).lower()
		if self.theme:
			theme = ET.SubElement(interface, 'theme')
			theme.text = str(self.theme)

		# Interface / Screen
		screen = ET.SubElement(interface, 'screen')
		screen_width = ET.SubElement(screen, 'width')
		screen_width.text = str(self.screen_width)
		screen_height = ET.SubElement(screen, 'height')
		screen_height.text = str(self.screen_height)
		rotation = ET.SubElement(screen, 'rotation')
		rotation.text = str(self.rotation)

		# Interface / Graphics
		graphics = ET.SubElement(interface, 'graphics')
		quality = ET.SubElement(graphics, 'quality')
		quality.text = str(self.get_gfx_quality_display()).lower()
		max_width = ET.SubElement(graphics, 'max-image-width')
		max_width.text = str(self.max_image_width)
		max_height = ET.SubElement(graphics, 'max-image-height')
		max_height.text = str(self.max_image_height)

		# Interface / Controls
		controls = ET.SubElement(interface, 'controls')
		for c in Control.objects.all():
			# Event / Name
			event = ET.SubElement(controls, 'event')
			name = ET.SubElement(event, 'name')
			name.text = str(c.get_event_display()).lower()

			# Event / Device
			device = ET.SubElement(event, 'device')
			device_type = ET.SubElement(device, 'type')
			device_type.text = str(c.get_device_type_display()).lower()
			device_id = ET.SubElement(device, 'id')
			device_id.text = str(c.device_id)

			# Event / Control
			control = ET.SubElement(event, 'control')
			control_type = ET.SubElement(control, 'type')
			control_type.text = str(c.get_control_type_display()).lower()
			control_id = ET.SubElement(control, 'id')
			control_id.text = str(c.control_id)

			# Event / Value
			value = ET.SubElement(event, 'value')
			value.text = str(c.value).lower()

		# Locations
		locations = ET.SubElement(root, 'locations')
		for l in Location.objects.all():
			location = ET.SubElement(locations, 'location')
			type = ET.SubElement(location, 'type')
			type.text = str(l.get_type_display()).lower()
			directory = ET.SubElement(location, 'directory')
			directory.text = str(l.provider.directory.path)

		return ET.tostring(root)

	def generate_config(self):
		if not self.config_dir:
			raise FrontEndException('No configuration directory set.')

		if not os.path.exists(self.config_dir):
			raise FrontEndException('No such file or directory.')

		if not os.path.isdir(self.config_dir):
			raise FrontEndException('Not a directory.')

		# Main config file.
		try:
			f = open(os.path.join(self.config_dir, 'config.xml'), 'w')
		except:
			raise FrontEndException('Unable to open file for writing.')

		xml = minidom.parseString(self.config())
		f.write(xml.toprettyxml())
		f.close()

		# Game lists in separate files.
		for gl in GameList.objects.all():
			try:
				f = open(os.path.join(self.config_dir, gl.file_name()), 'w')
			except:
				raise FrontEndException('Unable to open file for writing.')

			xml = minidom.parseString(gl.config())
			f.write(xml.toprettyxml())
			f.close()

