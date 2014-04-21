from django.db import models

RESOURCE_TYPES = (
	('b', 'Backgrounds'),
	('d', 'Data'),
	('g', 'Games'),
	('s', 'Screenshots'),
	('t', 'Titles'),
	('v', 'Videos'),
)

class Provider(models.Model):
	name = models.CharField(max_length=50)
	resource_type = models.CharField(max_length=1, choices=RESOURCE_TYPES)

	def __unicode__(self):
		return self.name

class ProviderException(Exception):
	def __init__(self, message):
		self.message = message

	def __unicode__(self):
		return self.message

