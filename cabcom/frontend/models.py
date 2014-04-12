from django.db import models
from cabcom.gamelist.models import Game, Genre, Platform, Publisher, ControlType

class FrontEnd(models.Model):
	def __unicode__(self):
		return self.name
