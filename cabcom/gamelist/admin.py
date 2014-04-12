from django.contrib import admin
from cabcom.gamelist.models import Game, Data, Genre, Platform, Publisher, ControlType

class GameAdmin(admin.ModelAdmin):
	list_display = ['display_name','name','file_name','genre','platform','publisher','release_date']
	ordering = ['display_name']

admin.site.register(Game, GameAdmin)
admin.site.register(Data, GameAdmin)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)
admin.site.register(ControlType)

