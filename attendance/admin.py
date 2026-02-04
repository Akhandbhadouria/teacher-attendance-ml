from django.contrib import admin
from .models import User, Attendance, Timetable, LectureAttendance

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

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'day_of_week', 'start_time', 'end_time', 'subject')
    list_filter = ('day_of_week', 'teacher')
    search_fields = ('teacher__name', 'subject')

@admin.register(LectureAttendance)
class LectureAttendanceAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'timetable', 'date', 'status', 'time')
    list_filter = ('date', 'status', 'teacher')
    date_hierarchy = 'date'
