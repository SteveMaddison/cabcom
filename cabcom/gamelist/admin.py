from django.contrib import admin
from cabcom.gamelist.models import Game, Data, Genre, Platform, Publisher, ControlType, Filter

class DataAdmin(admin.ModelAdmin):
	list_display = ['display_name','name','file_name','genre','platform','publisher','release_date']
	ordering = ['display_name']

def populate(modeladmin, request, queryset):
	short_description = 'Populate'
	updated = 0

	for p in queryset:
		if p.populate():
			updated += 1

	modeladmin.message_user(request, str(updated) + ' items updated')

class GameAdmin(DataAdmin):
	actions = [populate]

admin.site.register(Game, GameAdmin)
admin.site.register(Data, DataAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)
admin.site.register(ControlType)
admin.site.register(Filter)

