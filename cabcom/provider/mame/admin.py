from django.contrib import admin
from cabcom.provider.mame.models import Mame
from cabcom.provider.admin import ProviderAdmin

admin.site.register(Mame, ProviderAdmin)

