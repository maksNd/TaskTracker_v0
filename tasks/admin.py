from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'created_by')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'created_by__username')
    ordering = ('-created_at',) 