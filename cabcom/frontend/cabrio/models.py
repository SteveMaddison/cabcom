from django.db import models
from cabcom.frontend.models import FrontEnd, FrontEndException
from cabcom.gamelist.models import Game, Filter
from cabcom.provider.directory.models import Directory
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import os, errno
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
	(0,   '0'),
	(90,  '90'),
	(180, '180'),
	(270, '270'),
)

GFX_VALUES = (
	('l', 'Low'),
	('m', 'Medium'),
	('h', 'High'),
)

LOCATION_TYPES = {
	'b': 'background',
	's': 'screenshot',
	't': 'logo',
	'v': 'video',
}

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
		for g in self.games():
			game = ET.SubElement(games, 'game')
			name = ET.SubElement(game, 'name')

			if g.display_name:
				name.text = str(g.display_name)
			else:
				name.text = str(g.name)

			rom = ET.SubElement(game, 'rom-image')
			rom.text = str(g.file_name)

			if g.platform:
				platform = ET.SubElement(game, 'platform')
				platform.text = str(g.platform)

			categories = ET.SubElement(game, 'categories')

			if g.genre:
				category = ET.SubElement(categories, 'category')
				name = ET.SubElement(category, 'name')
				name.text = 'Genre'
				value = ET.SubElement(category, 'value')
				value.text = str(g.genre)

			if g.publisher:
				category = ET.SubElement(categories, 'category')
				name = ET.SubElement(category, 'name')
				name.text = 'Publisher'
				value = ET.SubElement(category, 'value')
				value.text = str(g.publisher)

			if g.control_types.count() > 0:
				for c in g.control_types.all():
					category = ET.SubElement(categories, 'category')
					name = ET.SubElement(category, 'name')
					name.text = 'Control'
					value = ET.SubElement(category, 'value')
					value.text = str(c)

		return ET.tostring(root)

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
		for l in Directory.objects.filter(resource_type__in = ['b','s','t','v']):
			location = ET.SubElement(locations, 'location')
			type = ET.SubElement(location, 'type')
			type.text = LOCATION_TYPES[l.resource_type]
			directory = ET.SubElement(location, 'directory')
			directory.text = str(l.path)

		return ET.tostring(root)

	def generate_config(self):
		if not self.config_dir:
			raise FrontEndException('No configuration directory set.')

		if not os.path.exists(self.config_dir):
			try:
				os.makedirs(self.config_dir)
			except OSError as e:
				if e.errno == errno.EXIST and os.path.isdir(self.config_dir):
					pass
				else:
					raise FrontEndException('Unable to create directory.')

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

		if GameList.objects.exists():
			# Configured game lists in separate files.
			for gl in GameList.objects.all():
				try:
					f = open(os.path.join(self.config_dir, gl.file_name()), 'w')
				except:
					raise FrontEndException('Unable to open file for writing.')
	
				xml = minidom.parseString(gl.config())
				f.write(xml.toprettyxml())
				f.close()
		else:
			# Create a temporary list containing all games.
			all_games = GameList(filter = None)
			all_games.save()

			try:
				f = open(os.path.join(self.config_dir, 'games.xml'), 'w')
			except:
				raise FrontEndException('Unable to open file for writing.')

			xml = minidom.parseString(all_games.config())
			f.write(xml.toprettyxml())
			f.close()

			all_games.delete()

