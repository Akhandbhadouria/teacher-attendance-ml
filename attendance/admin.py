from django.contrib import admin
from .models import User, Attendance

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone', 'registered_at')
    search_fields = ('user_id', 'name', 'email')
    list_filter = ('registered_at',)
    ordering = ('-registered_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'time', 'timestamp')
    search_fields = ('user__name', 'user__user_id')
    list_filter = ('date',)
    ordering = ('-timestamp',)
    date_hierarchy = 'date'
