from django.contrib import admin
from cabcom.provider.models import Provider

def refresh(modeladmin, request, queryset):
	for p in queryset:
		p.refresh()

refresh.short_description = 'Refresh'

class ProviderAdmin(admin.ModelAdmin):
	list_display = ['name']
	ordering = ['name']
	actions = [refresh]

