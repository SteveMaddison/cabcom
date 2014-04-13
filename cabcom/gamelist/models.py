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
	def populate(self, replace = True):
		updated = False

		# TODO: handle multiple matches.
		data = Data.objects.filter(name = self.name).first()
		if data:
			if replace or not self.display_name:
				self.display_name = data.display_name
				updated = True
			if replace or not self.genre:
				self.genre = data.genre
				updated = True
			if replace or not self.publisher:
				self.publisher = data.publisher
				updated = True
			if replace or not self.release_date:
				self.release_date = data.release_date
				updated = True
			if replace or not self.platform:
				self.platform = data.platform
				updated = True
			if replace or not self.control_types.all():
				self.control_types.all().delete()
				for control_type in data.control_types.all():
					self.control_types.add(control_type)
				updated = True

			self.save()

		return updated

class Filter(models.Model):
	name = models.CharField(max_length = 50)
	genres = models.ManyToManyField(Genre, blank = True, null = True)
	publishers = models.ManyToManyField(Publisher, blank = True, null = True)
	platforms = models.ManyToManyField(Platform, blank = True, null = True)
	control_types = models.ManyToManyField(ControlType, blank = True, null = True)
	providers = models.ManyToManyField('provider.Provider', blank = True, null = True)

	def __unicode__(self):
		return self.name

