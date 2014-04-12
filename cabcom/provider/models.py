from django.db import models

RESOURCE_TYPES = (
	('g', 'Games'),
	('i', 'Images'),
	('v', 'Videos'),
	('d', 'Data'),
)

class Provider(models.Model):
	name = models.CharField(max_length=50, unique=True)
	resource_type = models.CharField(max_length=1, choices=RESOURCE_TYPES)

	def __unicode__(self):
		return self.name

class ProviderException(Exception):
	def __init__(self, message):
		self.message = message

	def __unicode__(self):
		return self.message

