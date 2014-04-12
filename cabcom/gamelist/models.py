from django.db import models

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
	name = models.CharField(max_length=50)
	display_name = models.CharField(max_length=128)
	genre = models.ForeignKey(Genre, blank=True, null=True)
	publisher = models.ForeignKey(Publisher, blank=True, null=True)
	release_date = models.DateTimeField(blank=True, null=True)
	platform = models.ForeignKey(Platform, blank=True, null=True)
	provider = models.ForeignKey('provider.Provider')

	def __unicode__(self):
		return self.name

class List(models.Model):
	name = models.CharField(max_length=50)
	games = models.ManyToManyField(Game, blank=True, null=True)

	def __unicode__(self):
		return self.name

