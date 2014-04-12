from django.db import models

class Genre(models.Model):
	name = models.CharField(max_length = 50, unique = True)

	def __unicode__(self):
		return self.name

class Platform(models.Model):
	name = models.CharField(max_length = 50, unique = True)

	def __unicode__(self):
		return self.name

class Publisher(models.Model):
	name = models.CharField(max_length = 50, unique = True)

	def __unicode__(self):
		return self.name

class ControlType(models.Model):
	name = models.CharField(max_length = 50, unique = True)

	def __unicode__(self):
		return self.name

class GameData(models.Model):
	name = models.CharField(max_length = 50)
	display_name = models.CharField(max_length = 128)
	file_name = models.CharField(max_length = 50)
	genre = models.ForeignKey(Genre, blank = True, null = True)
	publisher = models.ForeignKey(Publisher, blank = True, null = True)
	release_date = models.DateField(blank = True, null = True)
	platform = models.ForeignKey(Platform, blank = True, null = True)
	control_types = models.ManyToManyField(ControlType, blank = True, null = True)
	provider = models.ForeignKey('provider.Provider')

	class Meta:
		abstract = True

	def __unicode__(self):
		return self.name

class Data(GameData):
	pass

class Game(GameData):
	pass
