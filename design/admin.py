from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip', 'code', 'created']
    list_filter = ['ip']
    search_fields = ['ip']
