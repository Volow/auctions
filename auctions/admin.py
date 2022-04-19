from django.contrib import admin

# Register your models here.

from .models import User, Catigory, Lot

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("lot_owner",)

# Register your models here.

admin.site.register(User)
admin.site.register(Catigory)
admin.site.register(Lot)
