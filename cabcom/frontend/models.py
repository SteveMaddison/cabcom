from django.db import models

class FrontEnd(models.Model):

	def __unicode__(self):
		return self.name

