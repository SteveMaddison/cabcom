from django.contrib import admin
from cabcom.frontend.cabrio.models import Cabrio, Control, Theme, GameList
from cabcom.frontend.admin import FrontEndAdmin

admin.site.register(Cabrio, FrontEndAdmin)
admin.site.register(Control)
admin.site.register(Theme)
admin.site.register(GameList)

