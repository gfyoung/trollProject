from django.contrib import admin
from .models import Download

class DownloadAdmin(admin.ModelAdmin):
    list_display = ("target_os", "filename", "description")
    list_filter = ("target_os", "filename", "description")

admin.site.register(Download, DownloadAdmin)
