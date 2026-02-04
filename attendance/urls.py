from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('users/', views.users_list, name='users_list'),
    path('users/<str:user_id>/', views.user_detail, name='user_detail'),
    path('users/<str:user_id>/delete/', views.delete_user, name='delete_user'),
    path('users/<str:user_id>/timetable/', views.manage_timetable, name='manage_timetable'),
    path('timetable/delete/<int:slot_id>/', views.delete_timetable_slot, name='delete_timetable_slot'),
    path('attendance/', views.attendance_records, name='attendance_records'),
    path('register/', views.register_page, name='register_page'),
    path('register/submit/', views.register_user, name='register_user'),
    path('mark-attendance/', views.mark_attendance_page, name='mark_attendance_page'),
    path('mark-attendance/process/', views.process_attendance, name='process_attendance'),
    path('statistics/', views.statistics, name='statistics'),
    
    # Teacher Portal
    path('portal/login/', views.teacher_login, name='teacher_login'),
    path('portal/logout/', views.teacher_logout, name='teacher_logout'),
    path('portal/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('portal/mark/<int:timetable_id>/', views.mark_lecture_attendance, name='mark_lecture_attendance'),
]
