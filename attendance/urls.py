from django.urls import path

# Attendance app ke views import
from .views import (
    mark_attendance,
    student_attendance,
    monthly_attendance_report
)

# ======================================================
# Attendance App URL Configuration
# ======================================================
# Ye file attendance module ke saare routes define karti hai
# Saare URLs main project ke urls.py me include honge:
# path('attendance/', include('attendance.urls'))
# ======================================================

urlpatterns = [

    # --------------------------------------------------
    # 👨‍🏫 TEACHER
    # --------------------------------------------------
    # Daily attendance mark karne ka page
    # Sirf TEACHER role access kar sakta hai
    #
    # Full URL:
    # /attendance/mark/
    # --------------------------------------------------
    path(
        'mark/',
        mark_attendance,
        name='mark_attendance'
    ),

    # --------------------------------------------------
    # 👨‍🎓 STUDENT
    # --------------------------------------------------
    # Student apni hi attendance dekh sakta hai
    #
    # Full URL:
    # /attendance/my/
    # --------------------------------------------------
    path(
        'my/',
        student_attendance,
        name='student_attendance'
    ),

    # --------------------------------------------------
    # 📊 ADMIN / TEACHER
    # --------------------------------------------------
    # Monthly attendance report
    # Month aur year query params se aate hain
    #
    # Example:
    # /attendance/monthly-report/?month=7&year=2025
    # --------------------------------------------------
    path(
        'monthly-report/',
        monthly_attendance_report,
        name='monthly_attendance_report'
    ),
]
