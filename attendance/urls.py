from django.urls import path

# Attendance app ke views import kar rahe hain
from .views import (
    mark_attendance,
    student_attendance,
    monthly_attendance_report
)

# ======================================================
# Attendance App URLs
# ======================================================
urlpatterns = [

    # 👨‍🏫 Teacher ke liye:
    # Daily attendance mark karne ka page
    # URL: /attendance/mark/
    path(
        'mark/',
        mark_attendance,
        name='mark_attendance'
    ),

    # 👨‍🎓 Student ke liye:
    # Apni attendance dekhne ka page
    # URL: /attendance/my/
    path(
        'my/',
        student_attendance,
        name='student_attendance'
    ),

    # 📊 Admin / Teacher ke liye:
    # Monthly attendance report dekhne ka page
    # URL: /attendance/monthly-report/
    # Example: /attendance/monthly-report/?month=7&year=2025
    path(
        'monthly-report/',
        monthly_attendance_report,
        name='monthly_attendance_report'
    ),
]
