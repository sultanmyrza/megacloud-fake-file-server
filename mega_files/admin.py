from django.contrib import admin

from .models import MegaBinary, MegaFile


@admin.register(MegaBinary)
class MegaBinaryAdmin(admin.ModelAdmin):
    pass


@admin.register(MegaFile)
class MegaFileAdmin(admin.ModelAdmin):
    list_display = ["fileName", "serverFileName", "binary"]
    readonly_fields = ["serverFileName"]
