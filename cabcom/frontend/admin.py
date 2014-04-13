from django.contrib import admin, messages
from cabcom.frontend.models import FrontEndException

def generate_config(modeladmin, request, queryset):
	short_description = 'Generate Config'
	generated = 0

	for fe in queryset:
		try:
			fe.generate_config()
			generated += 1
		except FrontEndException as e:
			msg = str(fe) + ': ' + e.message
			modeladmin.message_user(request, msg, messages.ERROR)

	modeladmin.message_user(request, str(generated) + ' configurations generated')

class FrontEndAdmin(admin.ModelAdmin):
	actions = [generate_config]

