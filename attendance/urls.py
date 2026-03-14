from django.urls import path
from .views import (
    mark_attendance,
    student_attendance,
    monthly_attendance_report,
)

# Namespace (important for template urls)
app_name = "attendance"

urlpatterns = [

    # Teacher – Mark student attendance
    path(
        "teacher/mark-attendance/",
        mark_attendance,
        name="mark_attendance"
    ),

    # Student – View own attendance
    path(
        "my-attendance/",
        student_attendance,
        name="student_attendance"
    ),

    # Admin / Teacher – Monthly attendance report
    path(
        "monthly-report/",
        monthly_attendance_report,
        name="monthly_attendance_report"
    ),
]