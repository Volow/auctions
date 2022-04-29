from django.contrib import admin

# Register your models here.

from .models import *

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("lot_owner",)

# Register your models here.

admin.site.register(User)
admin.site.register(Catigory)
admin.site.register(Lot)
admin.site.register(Comment)
admin.site.register(Bid)
admin.site.register(WatchList)
