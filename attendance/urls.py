from django.urls import path
from .views import (
    mark_attendance,
    student_attendance,
    monthly_attendance_report,
)

urlpatterns = [

    # 👨‍🏫 Teacher – mark attendance
    path(
        'teacher/mark-attendance/',
        mark_attendance,
        name='mark_attendance'
    ),

    # 👨‍🎓 Student – view own attendance
    path(
        'my/',
        student_attendance,
        name='student_attendance'
    ),

    # 📊 Admin / Teacher – monthly report
    path(
        'monthly-report/',
        monthly_attendance_report,
        name='monthly_attendance_report'
    ),
]
