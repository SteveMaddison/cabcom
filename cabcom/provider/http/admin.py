from django.contrib import admin
from cabcom.provider.http.models import Http
from cabcom.provider.admin import ProviderAdmin

admin.site.register(Http, ProviderAdmin)

