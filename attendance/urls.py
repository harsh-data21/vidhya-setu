from django.urls import path
from .views import mark_attendance, student_attendance, monthly_attendance_report

urlpatterns = [
    path('mark/', mark_attendance, name='mark_attendance'),
    path('my/', student_attendance, name='student_attendance'),
     path('monthly-report/', monthly_attendance_report, name='monthly_attendance_report'),
]
