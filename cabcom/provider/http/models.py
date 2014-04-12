from django.db import models
from cabcom.provider.models import Provider

class Http(Provider):
	url = models.CharField(max_length=256)

	class Meta:
		verbose_name = 'HTTP Provider'

	def __unicode__(self):
		return self.name

