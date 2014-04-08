from django.db import models
from cabcom.provider.models import Provider

class Directory(Provider):
	path = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Directory Provider'

	def __unicode__(self):
		return self.name

