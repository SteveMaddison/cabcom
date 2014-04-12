from django.contrib import admin, messages
from cabcom.provider.models import Provider, ProviderException

def refresh(modeladmin, request, queryset):
	try:
		for p in queryset:
			p.refresh()
	except ProviderException as e:
		msg = str(p) + ': ' + e.message
		modeladmin.message_user(request, msg, messages.ERROR)

refresh.short_description = 'Refresh'

class ProviderAdmin(admin.ModelAdmin):
	list_display = ['name','resource_type']
	ordering = ['name']
	actions = [refresh]

