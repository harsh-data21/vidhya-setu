from django.urls import path
from .views import (
    home,
    login_view,
    logout_view,
    admin_dashboard,
    teacher_dashboard,
    student_dashboard,
    add_homework,
    view_homework,
)

urlpatterns = [
    # Home & Auth
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Role-based dashboards
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),

    #  Homework URLs
    path('teacher/add-homework/', add_homework, name='add_homework'),
    path('student/homework/', view_homework, name='view_homework'),
]
