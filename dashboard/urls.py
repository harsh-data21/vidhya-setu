from django.urls import path
from . import views

urlpatterns = [

    # ================= ADMIN =================
    path('admin/', views.admin_dashboard, name='admin_dashboard'),

    # ================= TEACHER =================
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teacher/marks/', views.teacher_marks, name='teacher_marks'),

    # ================= STUDENT =================
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('student/attendance/', views.student_attendance, name='student_attendance'),
    path('student/marks/', views.student_marks, name='student_marks'),

]
