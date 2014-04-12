from django.db import models
from cabcom.gamelist.models import List

class FrontEnd(models.Model):
	gamelists = models.ManyToManyField(List, blank = True, null = True)

	def __unicode__(self):
		return self.name

