from django.contrib import admin
from cabcom.gamelist.models import List, Game, Genre, Platform, Publisher

admin.site.register(List)
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Publisher)

