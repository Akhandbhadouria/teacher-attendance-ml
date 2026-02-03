from django.db import models
from django.utils import timezone

class User(models.Model):
    """User model for storing registered users"""
    user_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
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
