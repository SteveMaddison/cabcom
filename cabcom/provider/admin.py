from django.contrib import admin, messages
from cabcom.provider.models import Provider, ProviderException

def refresh(modeladmin, request, queryset):
	short_description = 'Refresh'
	added = 0

	try:
		for p in queryset:
			added += p.refresh()
	except ProviderException as e:
		msg = str(p) + ': ' + e.message
		modeladmin.message_user(request, msg, messages.ERROR)

	modeladmin.message_user(request, str(added) + ' items added')

class ProviderAdmin(admin.ModelAdmin):
	list_display = ['name','resource_type']
	ordering = ['name']
	actions = [refresh]

