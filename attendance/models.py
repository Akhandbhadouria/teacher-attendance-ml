from django.db import models
from django.utils import timezone

class User(models.Model):
    """User model for storing registered users"""
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=128, default='123456')
    registered_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'attendance_user'
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.name} ({self.user_id})"

class Attendance(models.Model):
    """Attendance model for storing attendance records"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'attendance_record'
        ordering = ['-timestamp']
        unique_together = ['user', 'date']  # One attendance per user per day
    
    def __str__(self):
        return f"{self.user.name} - {self.date}"

class Timetable(models.Model):
    DAYS_OF_WEEK = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetable')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
        
    def __str__(self):
        return f"{self.teacher.name} - {self.get_day_of_week_display()} ({self.subject})"

class LectureAttendance(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Present')
    
    class Meta:
        unique_together = ['timetable', 'date']

    def __str__(self):
        return f"{self.teacher.name} - {self.timetable.subject} - {self.date}"
