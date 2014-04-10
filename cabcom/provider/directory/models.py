from django.db import models
from cabcom.provider.models import Provider, ProviderException
import os

class Directory(Provider):
	path = models.CharField(max_length=128)

	class Meta:
		verbose_name = 'Directory Provider'

	def __unicode__(self):
		return self.name

	def list(self):
		if not self.path:
			raise ProviderException('Path not set.')

		if not os.path.exists(self.path):
			raise ProviderException('No such file or directory.')

		if not os.path.isdir(self.path):
			raise ProviderException('Not a directory.')

		return os.listdir(self.path)

