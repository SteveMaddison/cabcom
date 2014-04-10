from django.contrib import admin
from cabcom.provider.directory.models import Directory
from cabcom.provider.admin import ProviderAdmin

admin.site.register(Directory, ProviderAdmin)

