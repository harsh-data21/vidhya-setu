from django.urls import path, include   # ✅ include add kiya

from .views import (
    home,
    login_view,
    logout_view,

    # Dashboards
    admin_dashboard,
    teacher_dashboard,
    student_dashboard,

    # Student Registration
    student_register,

    # Homework
    add_homework,
    view_homework,
)

urlpatterns = [

    # 🏠 HOME & AUTH
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # 📊 DASHBOARDS
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher-dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),

    # 🎓 STUDENT REGISTRATION
    path('register/student/', student_register, name='student_register'),

    # 📚 HOMEWORK
    path('teacher/add-homework/', add_homework, name='add_homework'),
    path('student/homework/', view_homework, name='view_homework'),

    # 💰 FEES MODULE
    path('fees/', include('fees.urls')),
]
