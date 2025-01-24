from django.contrib import admin
from .models import Task, Project, User

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'due_date')  # Columns to display in the Task admin list view
    search_fields = ('title',)  # Search bar to filter tasks by title

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date')  # Columns to display in the Project admin list view

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')

