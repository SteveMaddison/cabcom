from django.db import models
from cabcom.gamelist.models import Game, Genre, Platform, Publisher, ControlType

class FrontEnd(models.Model):
	def __unicode__(self):
		return self.name

class FrontEndException(Exception):
	def __init__(self, message):
		self.message = message

	def __unicode__(self):
		return self.message

