from django.contrib import admin

from .models import MegaRate, MegaUser


@admin.register(MegaRate)
class MegaRateAdmin(admin.ModelAdmin):
    pass


@admin.register(MegaUser)
class MegaUserAdmin(admin.ModelAdmin):
    pass
