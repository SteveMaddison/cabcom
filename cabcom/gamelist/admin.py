from django.contrib import admin
from cabcom.gamelist.models import List, Game, Genre, Platform, Publisher

class GameAdmin(admin.ModelAdmin):
	list_display = ['display_name','name','genre','platform','publisher']
	ordering = ['display_name']

admin.site.register(List)
admin.site.register(Game, GameAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)

