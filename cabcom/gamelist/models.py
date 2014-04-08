from django.db import models
from cabcom.provider.models import Provider

class List(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Genre(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Publisher(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

class Game(models.Model):
	name = models.CharField(max_length=128)
	genre = models.ForeignKey(Genre)
	publisher = models.ForeignKey(Publisher)
	release_date = models.DateTimeField()
	platform = models.ForeignKey(Platform)
	gamelist = models.ManyToManyField(List)
	provider = models.ForeignKey(Provider)

	def __unicode__(self):
		return self.name

